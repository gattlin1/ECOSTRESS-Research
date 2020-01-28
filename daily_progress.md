# Daily Progress Journal

## January 19, 2020

1. Rewrote Hitlist implementation with classes. This way it'll be easier to have multiple different versions for spectral similarity algorithms.

## January 21, 2020

1. Worked on the spectrum matcher only matching values if their wavelengths are withing a certain threshold of each other.
    - Hopefully this will fix the issues where two spectrum with different wavelength ranges end up making the similarity algorithms fail
2. Fixed the issue with some of the text files having characters that are able to be parsed.
    - ex. Like the degree symbol

## January 23, 2020

1. Started work on single pass pearson correlation coefficient
    - The current pearson implementation must make two passes. First to get the average and the second to calculate the formula. The implementation now will do this in one pass and save on computations
2. Starting to have the actual hitlist give back results for the NASA dataset. Only have tested it on a few random spectrum so far.
3. Fixed the Results Generator for the NASA dataset.

## January 26, 2020

1. Graphed all NASA spectrum.
2. Started organizing the dataset to ab pairs.
