import random
from scipy import stats
import numpy as np
import math
N = 8192
PS = [0.2, 0.4, 0.6, 0.8]
BS = [32, 256, 1024, 8192]
M = 5

def produce_seqs():
    xk = [0,1]
    seqs = []
    for i in range(len(PS)):
        p=PS[i]
        pk = (1-p, p)
        dist = stats.rv_discrete(values=(xk,pk))
        list_seq = dist.rvs(size=N).tolist()
        list_seq_str = list(map(lambda x: str(x), list_seq))
        seq = ''.join(list_seq_str)
        seqs.append(seq)
    return seqs

def encode_sequence(seq, B):
    block = ""
    blocks = []
    S = 0
    E = 0
    for i in seq:
        block += str(i)
        if len(block) == B:
            blocks.append(block)
            block = ""

    encoded_blocks = [""] * len(blocks)
    for bl_n, block in enumerate(blocks):
        k = 0
        for i in block:
            if i == '1':
                encoded_blocks[bl_n] += str(k)
                k = 0
                S+=1
            elif k == M-1:
                encoded_blocks[bl_n] += str(k+1)
                k = 0
                S+=1
            else:
                k += 1
        if k != 0:
            encoded_blocks[bl_n] += block[B-k:]
            E+=k
    return encoded_blocks, S, E


def decode_sequence(encoded_seq):
    decoded_seq= ""
    for block in encoded_seq:
        for k in block:
            decoded_seq += "0"*int(k)
            if k != M:
                decoded_seq += "1"

    return decoded_seq

            
#TODO Resolve extra bit issue
def main():
    seqs = produce_seqs()
    enc_seq, S, E = encode_sequence(seqs[0], BS[0])
    dec_seq = decode_sequence(enc_seq)
    print(seqs[0], "\n")
    print(enc_seq)
    print(dec_seq)
    # for np, seq in enumerate(seqs):
    #     for B in BS:
    #         encoded_seq, S, E = encode_sequence(seq, B)
    #         # print(encoded_seq)
    #         bitrate = 1/N * (S * math.log2(M+1) + E)
    #         # print("B=", B, "p=", PS[np], "bitrate= ", bitrate)
    #         correct = seq == decode_sequence(encoded_seq)
    #         print(correct)
    #     print("\n")
    # print(seqs[0])
    # print(encode_sequence(seqs[0], BS[0]))
            


if __name__ == main():
    main()