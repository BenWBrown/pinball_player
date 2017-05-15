import os
import neat
import numpy as np
import cv2
import time
import keypress
import utils
import pickle

timeout = 60
score_timeout = 10
match_thresh = 0.075 #anything below this threshold is considered a match
output_thresh = 0.95
no_velocity = -9999999, -9999999

keys = ['z', 'x', '.', '/']
#TODO: MOVE THIS TO SOME SORT OF UTILS LIBRARY

#open up the game and the camera
utils.open_camtwist()
utils.open_pinball()

#start recording with opencv cam
cap = cv2.VideoCapture(0)

#load kernel image for the ball
ball = cv2.imread('ball.png', 1)

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        #start a new game
        utils.new_game()

        #read from the camera
        ret, frame = cap.read()

        #find the ball in the image to determine the ball's starting location
        res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        starting_pos = min_loc

        print "starting location: " + str(starting_pos)
        start_time = time.time()
        last_pos = starting_pos
        valid_velocity = True

        while(True):
            t = time.time()
            if start_time + timeout < t:
                break

            ret, frame = cap.read()

            res = cv2.matchTemplate(frame, ball, cv2.TM_SQDIFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if min_val < match_thresh:
                current_pos = min_loc

                #press spacebar if the ball is ready to be launched
                if utils.points_within_dist(current_pos, starting_pos, 5):
                    keypress.tap(" ", 2)

                if valid_velocity:
                    velocity = (current_pos[0] - last_pos[0], current_pos[1] - last_pos[1])
                else:
                    velocity = no_velocity
                adjusted_pos = (min_loc[0] - starting_pos[0], min_loc[1] - starting_pos[1])
                inp = adjusted_pos + velocity
                output = net.activate(inp)
                for index, value in enumerate(output):
                    if value > output_thresh:
                        keypress.tap(keys[index])
                last_pos = current_pos

            valid_velocity = min_val < match_thresh


        ret, frame = cap.read()
        genome.fitness = utils.score(frame, starting_pos) #todo: divide by number of balls used

def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    #TODO: or load from pickle
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 4)

    local_dir = os.path.dirname(__file__)
    pickle_path = os.path.join(local_dir, 'population.pickle')
    with open(pickle_path, 'w') as f:
        pickle.dump(p, f)


    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))


    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-4') #not sure what this does yet

if __name__ == "__main__":
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    run(config_path)
