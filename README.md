### Introduction
Thank you for checking out my project! This program is designed to identify a target face out of other face images. For
example, from three images of different people and another target image of one of those three people the
program should be able to match the correct face to the target. This program is made almost entirely from scratch,
only using libraries for basic image processing (PIL) and array processing and display (NumPy, Pyplot).

### How to operate the program
The program currently includes images of Matt Damon, Bill Gates, and Tom Cruise (and a target image of each) for
demonstration, and feel free to run the program on those images. However, if you'd like to test other images just drag
them into the program files, then head over to image_sources.txt. Here, list the strings of the potential and test
images in quotes, then run test_match.py!

### Drawbacks of the program
Because this is almost entirely from scratch, this program has a couple significant drawbacks. Most
notably, images that are run in the program must be cropped to only the face - from just above the head to just below
the chin. Faces must also be generally straight on and facing the camera. The program is also relatively time-intensive,
especially for large images. Because of this, I recommend only using images on the smaller side (< 800x800 or so),
though if you don't mind the wait it will work with images of any size.