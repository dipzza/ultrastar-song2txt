from argparse import ArgumentParser
from pathlib import Path

import crepe
import numpy as np
import librosa as lbr

import song2txt.txt_parser.txt_parser as txt_parser
from song2txt.pitch_utils import notes_to_array, beat_to_ms, calculate_pitches

DEF_SUFFIX = '_pitched'


def main():
    par = ArgumentParser()
    par.add_argument('filepath',
                     help='path to the original UltraStar txt file.')
    par.add_argument('--output', '-o', default=None,
                     help='directory to save pitched txt file; '
                     'uses same directory as filepath by default.')
    par.add_argument('--confidence', '-c', type=float, default=0.7,
                     help='minimum confidence to use a pitch estimate')
    par.add_argument('--model-size', '-m', default='tiny',
                     choices=['tiny', 'small', 'medium', 'large', 'tiny'],
                     help='model size for pitch estimation; smaller models '
                          'are faster but may be less accurate. Default: full')
    par.add_argument('--viterbi', '-v', action='store_true',
                     help='perform Viterbi decoding to smooth the pitch')
    par.add_argument('--step-size', '-s', type=int, default=10,
                     help='step size in ms for pitch estimation. Default: 10')
    args = par.parse_args()

    txt_path = Path(args.filepath)
    us_txt = txt_parser.read_file(txt_path)
    samples, sr = lbr.load(txt_path.parent / us_txt.metadata.mp3, sr=None)

    _, freq, conf, _ = crepe.predict(samples, sr,
                                     model_capacity=args.model_size,
                                     viterbi=args.viterbi,
                                     step_size=args.step_size)

    notes = us_txt.get_notes()
    notes_arr = notes_to_array(notes)
    notes_arr = beat_to_ms(notes_arr, us_txt.metadata.bpm, us_txt.metadata.gap)
    intervals = np.int_(notes_arr[:, :2] / args.step_size)
    pitches = calculate_pitches(freq, conf, intervals, args.confidence)

    for note, pitch in zip(notes, pitches):
        note.pitch = pitch

    if args.output is None:
        output_path = txt_path.with_stem(txt_path.stem + DEF_SUFFIX)
        txt_parser.write_file(us_txt, output_path)
    else:
        output_path = Path(args.output)
        txt_parser.write_file(us_txt, output_path)
