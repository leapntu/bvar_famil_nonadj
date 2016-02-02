from psychopy import visual, core, event, gui, sound
import pyglet, os, random

condition = 'not set'
conditionCount = {}
for line in open('conditionCounter.txt'):
    line = line.strip().split(',')
    conditionCount[ line[0] ] = int(line[1])

if conditionCount['varset'] <= conditionCount['scramble']:
    condition = 'varset'
else:
    condition = 'scramble'

fam_varset_root = './stimuli/famil_varset/' # path to folder containing movie stims, NOTE use final '/' so can be concatinated with file names to make full paths
fam_varset_paths = [ filename for filename in os.listdir(fam_varset_root) if not filename.startswith('.')] # get all file names in the movie folder set above (ignoring hidden files with list comprehension)
fam_varset_paths = [ (int(f.split('.')[0]),f) for f in fam_varset_paths]
fam_varset_paths = sorted(fam_varset_paths, key=lambda n: n[0])
fam_varset_paths = [ p for (n,p) in fam_varset_paths]
fam_varset_playlist = [] # create a placeholder for the movie stims created below to be itterated through

fam_scramble_root = './stimuli/famil_scramble/' # path to folder containing movie stims, NOTE use final '/' so can be concatinated with file names to make full paths
fam_scramble_paths = [ filename for filename in os.listdir(fam_scramble_root) if not filename.startswith('.')] # get all file names in the movie folder set above (ignoring hidden files with list comprehension)
fam_scramble_paths = [ (int(f.split('.')[0]),f) for f in fam_scramble_paths]
fam_scramble_paths = sorted(fam_scramble_paths, key=lambda n: n[0])
fam_scramble_paths = [ p for (n,p) in fam_scramble_paths]
fam_scramble_playlist = [] # create a placeholder for the movie stims created below to be itterated through

test_root = './stimuli/test/' # path to folder containing movie stims, NOTE use final '/' so can be concatinated with file names to make full paths
test_paths = [ filename for filename in os.listdir(test_root) if not filename.startswith('.')] # get all file names in the movie folder set above (ignoring hidden files with list comprehension)
test_paths = [ (int(f.split('.')[0]),f) for f in test_paths]
test_paths = sorted(test_paths, key=lambda n: n[0])
test_paths = [ p for (n,p) in test_paths]
test_playlist = [] # create a placeholder for the movie stims created below to be itterated through

get_root = './stimuli/get/'
get_paths = [ filename for filename in os.listdir(get_root) if not filename.startswith('.')] # get all file names in the movie folder set above (ignoring hidden files with list comprehension)
get_playlist = [] # create a placeholder for the movie stims created below to be itterated through


###CONSTANTS###

mode = '' # dummy variable to track program state condition
counting = 0 # set to zero when not counting how long the child has been looking away, and set to one if counting how long child has been looking away
look_away_time = 0 # when child looks away during test phase, get the time, and use it to keep checking if two seconds have passed

stim_start_stim = 0

get_done = 0 # flags the getter as being done or not

data = [] # to hold collected data points
key = pyglet.window.key # contains constants for key values, e.g. key.SPACE returns 32
win = visual.Window([1366,768]) # create psychopy window object
clock = core.MonotonicClock() # create sub-ms accurate clock that starts counting up from zero upon creation

info = [] # to hold initial metadata results
stimuli = '' # to hold current stimuli filename
look_onset = 0.0
click_stim = '' # to hold stimuli that was playing during click
space_down = 0.0 # create global place holder for clock time that space is pressed
space_time = 0.0 # crea                                  te global place holder for time space was pressed (space_down minus clock time when space is released)

data_root = './data/' # path to folder to write data
subject = str(len([ filename for filename in os.listdir(data_root) if not filename.startswith('.')]) + 1) # determine which subject this is by taking the number of data files in the directory (ignoring hidden files with list comprehension), adding one, and converting to string
# the writting of data files themselves is specified in the end of experiment section

famStart = 0
famStim = '' #stimuli at time of first press in famil phase

def writeData():
    conditionCount[condition] += 1
    counterFile = open('conditionCounter.txt','w')
    counterFile.write('varset,'+str(conditionCount['varset'])+'\n')
    counterFile.write('scramble,'+str(conditionCount['scramble']))
    counterFile.close()
    
    if info == [] or info[0] == '': #if metadata box was canceled or no subject name recoreded, set to 'unknown'
        info.append('unknown')
    
    output = open(data_root+subject+'_'+info[0]+'.csv','w') # generate output file name from collected info dialog and subject number
    
    header = 'subject, stim, rt, type\n'
    
    output.write(header)
    
    for (stim, rt, rt_type) in data:
        output.write(subject+','+stim+','+rt+','+rt_type+'\n')
    
    output.close()
    
    #os.system("files=./data/*_*;awk 'FNR==1 && NR!=1 { while (/^subj/) getline; }1 {print}' $files > plp_data.csv") # get list of data files and concatenate them to a single master file, using awk to remove unwanted headers
    
    print data
    

###EVENT HANDLERS###

# as per pyglet documentation, the following event logic is set for keydown and keyup events, respectively

def on_key_press(k,m):
    if k == key.SPACE:
        print 'space down'
        global space_down
        global stimuli
        global click_stim
        global famStim
        global look_onset
        global mode
        global counting
        global get_done
        if mode == "test" and counting == 1:
            counting = 0
            space_time = (clock.getTime() - look_away_time ) * 1000
            data.append( ( stimuli, str(space_time), "under2" ) )

        elif mode == 'get':
            get_done = 1
            mode = "test"
            look_onset = clock.getTime()
            space_down = clock.getTime()

        else:
            if mode == 'famil':
                click_stim = famStim
            elif mode == 'test' or mode == 'get':
                click_stim = stimuli
            look_onset = clock.getTime()
            space_down = clock.getTime()


def on_key_release(k,m):
    if k == key.SPACE:
        print 'space up'
        global writeData
        global space_down
        global space_time
        global famStim
        global data
        global click_stim
        global look_onset
        global mode
        global counting
        global look_away_time
        if mode == "test" and counting == 0:
            counting = 1
            look_away_time = clock.getTime()
        elif mode == "get":
            pass
        else:
            space_time = (clock.getTime() - space_down) * 1000 #return time in milliseconds
            print click_stim, famStim
            data.append(  ( click_stim+"~~"+famStim, str(space_time), "lookingFam" )  ) #data to be written to the output file is added to the data array above on each key release, and some globals are updated, i.e. 'stimuli' are updated as the experiment executes

    if k == key.ESCAPE:
        if mode == 'test':
            escStim = stimuli
        elif mode == 'famil':
            escStim = famStim
        data.append( ( escStim, str( (clock.getTime() - famStart) * 1000), "totalPlaying-Escape" ) )
        writeData()
        win.close()
        core.quit()

#pyglet window class instance is stored in the psyhopy.visual.Window object at winHandle
#the event handlers defined above must be added to it
#there are two event handler registration points: the low-level pyglet one inside the psychopy window, and the default psychopy.event
#the psychopy.event module is built on the underlying pyglet, so there seems to be no collisions

win.winHandle.push_handlers(on_key_press, on_key_release) #add event handlers defined above to the low-level pyglet event listener at winHandle

###LOAD STIMULI###

#Start Screen
start_background = test_background = visual.ImageStim(win, './stimuli/check.jpg')
fam_mov = visual.MovieStim(win, './stimuli/tsums.mp4', loop=True)
#test_background = visual.ImageStim(win, './stimuli/checkerboard.jpg')
start_text = visual.TextStim(win, text='Press S To Start', color='red')
ag = sound.Sound("./stimuli/ag.wav")

#Stims
for path in fam_varset_paths:
    fam_varset_playlist.append(sound.Sound(fam_varset_root+path))


for path in fam_scramble_paths:
    fam_scramble_playlist.append(sound.Sound(fam_scramble_root+path))


for path in test_paths:
    test_playlist.append(sound.Sound(test_root+path))

random.shuffle(test_playlist)

for path in get_paths:
    get_playlist.append(visual.MovieStim(win, get_root+path, loop=True))

###EXPERIMENT###

#Meta Data
myDlg = gui.Dlg(title="JWP's experiment")
myDlg.addText('Participant Information')
myDlg.addField('Name:')
myDlg.addField('Age:')
myDlg.addText('Experiment Information')
myDlg.addField('RA:')
myDlg.show()
if myDlg.OK:
    info = myDlg.data
else:
    print 'user cancelled'

#Start Screen
start_background.draw()
start_text.draw()
win.flip()
event.waitKeys(keyList=['s'])

#Play Familiarization

famStart = clock.getTime()
mode = 'famil'
def playSound(soundStim):
    global famStim
    famStim = soundStim.fileName.split('/')[-1]
    end = soundStim.getDuration()
    soundStim.play()
    start = clock.getTime()
    while clock.getTime() - start < end:
        fam_mov.draw()
        win.flip()
        continue
    soundStim.status = 0
    
    

if condition == 'varset':
    for stim in fam_varset_playlist[:]:
        playSound(stim)
        
elif condition == 'scramble':
    for stim in fam_scramble_playlist[:]:
        playSound(stim)

print("testing")
mode = 'test'
data.append( ( "NA", str( (clock.getTime() - famStart) * 1000), "totalPlaying-Fam" ) )
for i in range(8):
    print("testing", i)
    stimuli = test_playlist[i].fileName.split('/')[-1]
    stim = test_playlist[i]
    random.shuffle(get_playlist)
    get = get_playlist[0]
    get_done = 0
    mode = 'get'
    
    ag.play()
    
    while get_done != 1:
        get.draw()
        win.flip()
        
    ag.stop()
    getter_done = 0

    #Start processing a test stimuli
    end = stim.getDuration()
    start = clock.getTime()
    test_background.draw()
    win.flip()
    stim.play()

    while clock.getTime() - start < end: # play until the sound is done
        test_background.draw()
        win.flip()
        if clock.getTime() - start < 21.8:
            if counting == 1 and clock.getTime() - look_away_time < 2:
                print clock.getTime() - look_away_time
                continue
            elif counting == 1 and clock.getTime() - look_away_time >= 2:
                stim.stop()
                counting = 0
                space_time = (look_away_time - space_down ) * 1000
                data.append( ( stimuli, str(space_time), "over2" ) )
                break
            else:
                continue
        elif clock.getTime() - start >= 21.8:
            stim.stop()
            stim.status = 'done'
            break
    print 'time out'
    if stim.status == 'done' and counting == 0:
        space_time = (clock.getTime() - space_down ) * 1000
        data.append( ( stimuli, str(space_time), "full_look" ) )
    elif stim.status == 'done' and counting == 1:
        counting = 0
        space_time = (look_away_time - space_down ) * 1000
        data.append( ( stimuli, str(space_time), "end_while_away" ) )


mode = 'final'

while get_done != 1:
    get.draw()
    win.flip()
    for button in event.getKeys():
        if button in ['n']:
            get_done = 1

#End Of Experiment


writeData()

win.close()
core.quit()
