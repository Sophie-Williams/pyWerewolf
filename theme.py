#!/usr/bin/evn python

class Type:
    game        = 0     #messages relating to the game
    command     = 1     #messages relating to commands
    join        = 2     #messages relating to joining the game and the join command
    role        = 3     #messages relating to assigning the roles
    night       = 4     #messages relating to the night phase
    kill        = 5     #messages relating to the kill command
    see         = 6     #messages relating to the see command
    guard       = 7     #messages relating to the guard command
    day         = 8     #messages relating to the day phase
    vote        = 9     #messages relating to voting and the vote command
    die         = 10    #messages relating to players dying
    win         = 11    #messages relating to the winning of the game
    misc        = 12    #miscellaneous messages
    num         = 13    #num message types

    subtypes = [Game, Command, Join, Role, Night, Kill, See, Guard, Day, Vote, Die,
                Win, Misc]
    
    class Game:     #game type subtypes
        start           = 0 #message when a new game gets started
        started         = 1 #message when players tries to start game when one 
                            #is running alread
        join_starting   = 2 #message when player joins channel and game is in
                            #join phase
        join_running    = 3 #message when player joins channel and game is running
        join_none       = 4 #message when player joins channel and game is not running
        num             = 5 #num game subtypes

    class Command:  #command type subtypes
        unknown          = 0 #message when you enter an unknown command
        game_not_running = 1 #message when you enter a game command when a game
                             #isn't running
        num              = 2 #num command subtypes

    class Join:     #join type subtypes
        join    = 0 #message when you successfully join a game
        rejoin  = 1 #message when you try to join a game you already joined
        leave   = 2 #message when you leave a game in the joining phase
        nick    = 3 #message when you change your nick in joining phase
        ended   = 4 #message when you try to join when joining has ended
        end     = 5 #message when joining ends
        success = 6 #message when enough players have joined
        fail    = 7 #message when not enough players have joined
        num     = 8 #num join subtypes

    class Role:     #role type subtypes
        announce    = 0 #message to announce roles to players
        other       = 1 #message to tell other player of same role to player
        other_p     = 2 #same as above but plural
        count       = 3 #message to announce the number of each role
        count_p     = 4 #same as above but plural
        num         = 5 #num role subtypes

    class Night:    #night type subtypes
        first       = 0 #message when first night starts
        subsequent  = 1 #message when subsequent nights start
        task        = 2 #message to ask player to fullfil their task
        task_p      = 3 #same as above but plural
        num         = 4 #num night subtypes

    class Kill:     #kill type subtypes
        success         = 0 #message when kill command succeeds
        success_p       = 1 #same as above but plural
        not_night       = 2 #message when it's not night
        not_wolf        = 3 #message when you aren't a wolf
        invalid_format  = 4 #message when your kill command is invalidly formatted
        invalid_target  = 5 #message when your target isn't in the game
        invalid_target_wolf = 6 #message when your target is a wolf
        num             = 7 #num kill subtypes
        
    class See:      #see type subtypes
        success         = 0 #message when see command succeeds
        not_night       = 1 #message when it's not night
        not_seer        = 2 #message when you aren't a seer
        invalid_format  = 3 #message when your see command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        result          = 5 #message to announce the result of your sightings
        num             = 6 #num see subtypes

    class Guard:    #guard type subtypes
        success         = 0 #message when guard command succeeds
        not_night       = 1 #message when it's not night
        not_guardian    = 2 #message when you aren't a guardian
        invalid_format  = 3 #message when your guard command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        num             = 5 #num guard subtypes

    class Day:      #day type subtypes
        start   = 0 #message when day starts
        num     = 1 #num day subtypes
        
    class Vote:     #vote type subtypes
        start           = 0 #message when voting starts
        success         = 1 #message when vote command succeeds
        not_vote_time   = 2 #message when it's not voting time
        invalid_format  = 3 #message when yoru vote command is invalidly formatted
        invalid_target  = 4 #message when your target isn't in the game
        end             = 5 #message when voting ends
        tie             = 6 #message if there is a tie
        num             = 7 #num vote subtypes

    class Die:      #die type subtypes
        kill        = 0 #message to announce killing by wolves
        vote        = 1 #message to announce lynch killing
        not_voting  = 2 #message to announce death due to not voting for too many turns
        nick        = 3 #message to announce death due to nick change
        leave       = 4 #message to announce death due to leaving game
        num         = 5 #num die subtypes

    class Win:      #win type subtypes
        wolf        = 0 #message to announce win by wolves
        wolf_p      = 1 #same as above but plural
        villager    = 2 #message to announce win by villagers
        villager_p  = 3 #same as above but plural
        draw        = 4 #message to announce draw
        list_role   = 5 #message to announce player role
        list_role_p = 6 #same as above but plural
        num         = 7 #num win subtypes

    class Misc:     #misc type subtypes
        help        = 0 #message containing help information
        randplayer  = 1 #message to announce random player in game
        not_player  = 2 #message to tell user he's not in the game
        dead        = 3 #message to tell user he's dead
        num         = 4 #num misc subtypes
        
class Theme:
    pass
