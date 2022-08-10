import os
from argparse import ArgumentParser

import crepe
import numpy as np

import uspitch.txt_parser as txt
from .audio_utils import open_audio, calculate_pitches


def main():
    par = ArgumentParser()
    par.add_argument('filepath',
                     help='path to the original UltraStar txt file.')
    par.add_argument('--output', '-o', default=None,
                     help='directory to save pitched txt file; '
                     'uses same directory as filepath by default.')
    par.add_argument('--confidence', '-c', type=float, default=0.7,
                     help='minimum confidence to use a pitch estimate')
    par.add_argument('--model-size', '-m', default='full',
                     choices=['tiny', 'small', 'medium', 'large', 'full'],
                     help='model size for pitch estimation; smaller models '
                          'are faster but may be less accurate. Default: full')
    par.add_argument('--viterbi', '-v', action='store_true',
                     help='perform Viterbi decoding to smooth the pitch')
    par.add_argument('--step-size', '-s', type=int, default=10,
                     help='step size in ms for pitch estimation. Default: 10')
    args = par.parse_args()

    text, metadata, note_timing = txt.read_file(args.filepath)
    song_path = os.path.join(os.path.dirname(args.filepath), metadata['MP3'])
    samples, sr = open_audio(song_path)

    _, freq, conf, _ = crepe.predict(samples, sr,
                                     model_capacity=args.model_size,
                                     viterbi=args.viterbi,
                                     step_size=args.step_size)
    intervals = np.int_(txt.beat_to_ms(metadata, note_timing) / args.step_size)
    pitches = calculate_pitches(freq, conf, intervals, args.confidence)

    if args.output is None:
        root, extension = os.path.splitext(args.filepath)
        txt.write_file(root + '_pitched' + extension, text, pitches)
    else:
        txt.write_file(args.output, text, pitches)
