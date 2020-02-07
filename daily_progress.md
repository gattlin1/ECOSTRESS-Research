# Daily Progress Journal

## NLC WORK

#### January 19, 2020

1. Rewrote Hitlist implementation with classes. This way it'll be easier to have multiple different versions for spectral similarity algorithms.

#### January 21, 2020

1. Worked on the spectrum matcher only matching values if their wavelengths are withing a certain threshold of each other.
    - Hopefully this will fix the issues where two spectrum with different wavelength ranges end up making the similarity algorithms fail
2. Fixed the issue with some of the text files having characters that are able to be parsed.
    - ex. Like the degree symbol

### January 23, 2020

1. Started work on single pass pearson correlation coefficient
    - The current pearson implementation must make two passes. First to get the average and the second to calculate the formula. The implementation now will do this in one pass and save on computations
2. Starting to have the actual hitlist give back results for the NASA dataset. Only have tested it on a few random spectrum so far.
3. Fixed the Results Generator for the NASA dataset.

### January 26, 2020

1. Graphed all NASA spectrum.
2. Started organizing the dataset to ab pairs.
3. Working on setting up the dataset. The current script to find the ab pairs uses cor to find them in a given sample set. It doesn't work well on meteorites so I think I can just use msd or mad or dpn for those sets.

### January 27, 2020

1. Working on setting up the dataset. It's not perfect but I went through and labeled the ab pairs that don't work at all and removed them. Used msd for the special cases and now all of the ab pairs look a lot better.
2. Kicked off the first run. Will see the results next morning.

### January 28, 2020

1. Was able to get the first run through
2. Started analyzing and the vegetation spectra seem to be very similar (vswir versions). Looks like it is one of the reasons we have so many failing.

### January 29, 2020

1. Worked on seeing if I could improve the ab pairs any more. Nothing substantial found. Seems like we will need to do manual checks to get further improvements. Right now I have a config file for special cases that is used to run in the script.
2. Working on nlc wavelength partitioning. Finished it late in the day so wasn't confident in running it in the new test. Ran the second test with the improved dataset.
3. Added categorical data to the results so we can see the accuracy of each spectrum category

### January 30, 2020

1. Got 2nd test run results. They are better now `that the bad ab pairs are removed, but the vegetation still is throwing a wrench in things. For many it is counting as over half of the missed classifications.

### February 2, 2020

1. Finishing up the weird bugs for the nlc wavelength version. Should be able to run in the next test.
2. The runtime is still very high so I think I'm going to tweak the program so it can run in parallel. Hopefully this will enable us to do a lot of tests.

### February 4, 2020

1. Looked at some multiprocessing w/ Josh. Didn't do a lot coding wise but he definitely showed me where I need to go for the multiprocessing.

### February 5, 2020

1. Changed the way the hitlist works. Created a difference matrix to store the values so we aren't calculating the same score twice. This will save on some processing speed as well.

### February 6, 2020

1. Added multiprocessing. W/ how I implemented my hitlist. Had to tweak stuff a bit but now I can just pass each one off to it's own core. From what I've seen this should be faster than mapping them in between cores.
    - With this multiprocessing I want to create a heatmap. I don't feel we can really say these results are correct until we find the best input parameters for nlc (floor and width values). W/ this multiprocessing it should be possible it will just take some time since we will probably need to run the hitlists at least 100 - 1000ish times. Luckily I will be able to still work on the CNN while this is running and shouldn't affect my research too much.

## NEURAL NETWORK WORK