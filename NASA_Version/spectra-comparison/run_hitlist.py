import colorama
import os
from hitlist import Hitlist

def main():
    # initialize console color.
    colorama.init()

    # initialize hitlists for normal spectra comparison and nlc.
    normal_hitlist = Hitlist('cor')
    nlc_hitlist = Hitlist('nlc -> cor')

    # loop through spectrum files in a directory and find matches in the hitlist
    directory_path = '../ecospeclib-all/'
    for file in os.listdir(directory_path):
        if (file.endswith('.txt')):
            file_path = directory_path + file
            normal_hitlist.find_match(file_path, directory_path)
            nlc_hitlist.find_match(file_path, directory_path)

    normal_hitlist.accuracy()
    nlc_hitlist.accuracy()

main()