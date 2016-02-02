#! /bin/bash

# CREATE 4 PSEUDO-RANDOMIZED ORDERS OF TRAINED TEST-TRIALS
# order 1
sox p-l-j.wav v-w-t.wav p-f-j.wav v-k-t.wav p-w-j.wav v-l-t.wav p-k-j.wav v-f-t.wav 1.trained-test-trial.wav

# order 2
sox v-f-t.wav p-k-j.wav v-l-t.wav p-w-j.wav v-k-t.wav p-f-j.wav v-w-t.wav p-l-j.wav 2.trained-test-trial.wav

# order 3
sox p-w-j.wav v-w-t.wav p-k-j.wav v-k-t.wav p-l-j.wav v-l-t.wav p-f-j.wav v-f-t.wav 3.trained-test-trial.wav

# order 4
sox v-k-t.wav p-k-j.wav v-f-t.wav p-l-j.wav v-l-t.wav p-w-j.wav v-w-t.wav p-f-j.wav 4.trained-test-trial.wav


# CREATE 4 PSEUDO-RANDOMIZED ORDERS OF UNTRAINED TEST-TRIALS
# order 1
sox p-l-t.wav v-w-j.wav p-f-t.wav v-k-j.wav p-w-t.wav v-l-j.wav p-k-t.wav v-f-j.wav 1.untrained-test-trial.wav

# order 2
sox v-f-j.wav p-k-t.wav v-l-j.wav p-w-t.wav v-k-j.wav p-f-t.wav v-w-j.wav p-l-t.wav       2.untrained-test-trial.wav

# order 3
sox v-w-j.wav p-w-t.wav v-l-j.wav p-f-t.wav v-k-j.wav p-l-t.wav v-f-j.wav p-k-t.wav 3.untrained-test-trial.wav

# order 4
sox p-k-t.wav v-f-j.wav p-l-t.wav v-k-j.wav p-f-t.wav v-l-j.wav p-w-t.wav v-w-j.wav 4.untrained-test-trial.wav

#sox -m p-*-j.wav > i-hear-trained-voices.wav
#sox -m v-*-t.wav > i-hear-more-trained-voices.wav