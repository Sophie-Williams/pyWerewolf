#!/usr/bin/env python

from player import *
import config
from game_data import *
import random

class Game(object):
    def __init__(self, bot, who):
        self.irc = bot
        self.c  = bot.connection
        self.timers = bot.timers
        self.theme = Theme()
        self.players = {}
        self.wolves = []
        self.mode = Mode.join
        self._start(who)

    def _chan_message(self, message_list):
        self.irc.send_message(self.irc.channel,
                              self.theme.get_string(message_list))

    def _notice(self, who, message_list):
        self.irc.send_notice(who,
                             self.theme.get_string(message_list))

    def _add_player(self, who):
        self.players[who.lower()] = Player(who)

    def _rem_player(self, who):
        pass #TODO: remove player from player list and check if game ended

    def _check_win(self):
        return False#TODO: count num wolves and num villagers

    def _assign_roles(self):
        num_players     = len(self.players)
        num_wolves      = 2#num_players//5
        num_angels      = 1
        num_traitors    = 1
        num_guardians   = num_players//9
        num_seers       = num_players//6

        if num_wolves < 1:
            num_wolves = 1
        if num_seers < 1:
            num_seers = 1

        num_villagers   = num_players-num_wolves-num_angels-num_traitors- \
                            num_guardians-num_seers

        if num_villagers <= 0:
            num_villagers += num_angels
            num_angels = 0
            num_villagers += num_traitors
            num_traitors = 0

        roles = []
        for i in xrange(num_wolves):
            roles.append(Wolf())
        for i in xrange(num_angels):
            roles.append(Angel())
        for i in xrange(num_traitors):
            roles.append(Traitor())
        for i in xrange(num_guardians):
            roles.append(Guardian())
        for i in xrange(num_seers):
            roles.append(Seer())
        for i in xrange(num_villagers):
            roles.append(Villager())

        random.shuffle(roles)

        for i, player in enumerate(self.players.keys()):
            self.players[player].role = roles[i]
            print self.players[player].nick, self.theme.role_names[roles[i].role],
            print self.theme.role_names[roles[i].appears_as]
            role = roles[i].role
            who = self.players[player].nick
            self.theme.reset()
            self.theme.user = who
            if role == Role.villager:
                self._notice(who, self.theme.role_villager_message)
            elif role == Role.wolf:
                self.wolves.append(who)
                self._notice(who, self.theme.role_wolf_message)
            elif role == Role.seer:
                self._notice(who, self.theme.role_seer_message)
            elif role == Role.guardian:
                self._notice(who, self.theme.role_guardian_message)
            elif role == Role.angel:
                self._notice(who, self.theme.role_angel_message)

        if num_wolves >= 2:
            for i in xrange(len(self.wolves)):
                other_wolves = []
                for j in xrange(i):
                    other_wolves.append(self.wolves[j])
                for j in xrange(i+1, len(self.wolves)):
                    other_wolves.append(self.wolves[j])
                self.theme.reset()
                self.theme.user = self.wolves[i]
                who = self.wolves[i]
                self.theme.wolves = " ".join(other_wolves)
                if len(other_wolves) == 1:
                    self._notice(who, self.theme.role_other_wolf_message)
                else:
                    self._notice(who, self.theme.role_other_wolves_message)
        if num_wolves > 1:
            self.theme.reset()
            self.theme.num = str(num_wolves)
            self._chan_message(self.theme.role_num_wolves_message)
        if num_seers > 1:
            self.theme.reset()
            self.theme.num = str(num_seers)
            self._chan_message(self.theme.role_num_seers_message)
        if num_guardians > 1:
            self.theme.reset()
            self.theme.num = str(num_guardians)
            self._chan_message(self.theme.role_num_guardians_message)
        if num_angels > 1:
            self.theme.reset()
            self.theme.num = str(num_angels)
            self._chan_message(self.theme.role_num_angels_message)


    def _start(self, who):
        #register callbacks
        for cb in Commands.game:
            self.irc.callbacks.reg_callback(cb, getattr(self, cb))
        self.irc.callbacks.reg_leave_callback(self.player_leave)
        self.irc.callbacks.reg_nick_callback(self.player_nick)

        #setup game info
        self.theme.reset()
        self.theme.user = who
        self._chan_message(self.theme.game_start_message)
        self._add_player(who)
        self.timers.add_timer(15, self.join_end)

    def end(self):
        for cb in Commands.game:
            self.irc.callbacks.unreg_callback(cb)
        self.irc.callbacks.unreg_leave_callback()
        self.irc.callbacks.unreg_nick_callback()
        self.timers.remove_all()

    def join_end(self, t=None, t2=None):
        if len(self.players) >= 3:
            self.irc.reset_modes()
            self.irc.set_moderated()
            self.mode = Mode.processing
            self.theme.reset()
            self.theme.num = str(len(self.players))
            self._chan_message(self.theme.join_success_message)
            self._assign_roles()
            self.night_start()
        else:
            self.theme.reset()
            self._chan_message(self.theme.join_fail_message)
            self.irc.end_game()

    def night_start(self):
        #TODO: tell alive roles what to do
        self.timers.add_timer(15, self.night_end)
        pass

    def night_end(self):
        self.mode = Mode.processing
        #TODO: output results of night
        if not self._check_win():
            self.day_start()

    def day_start(self):
        #TODO: Voice alive people
        self.timers.add_timer(15, self.vote_start)
        pass

    def vote_start(self):
        #TODO: tell people how to vote
        self.timers.add_timer(15, self.vote_end)
        pass

    def vote_end(self):
        #TODO: unvoice everyone
        #TODO: tally votes
        #TODO: kill player
        #TODO: check win
        #TODO: start_night
        pass

    def join(self, who, args):
        if self.mode == Mode.join:
            if who.lower() not in self.players:
                self._add_player(who)
                self.theme.reset()
                self.theme.user = who
                self.theme.num  = str(len(self.players))
                self._chan_message(self.theme.join_new_message)
                if self.timers.get_timer(self.join_end).time_left < 10:
                    self.timers.get_timer(self.join_end).set_timeleft(10)
            else:
                self.theme.reset()
                self.theme.user = who
                self._notice(who, self.theme.join_old_message)
        else:
            self._notice(who, self.theme.join_ended_message)

    def vote(self, who, args):
        if len(args) == 1:
            if self.mode == Mode.day_vote:
                #TODO: update vote and output
                pass
            else:
                #TODO: output not valid time
                pass
        else:
            #TODO: output invalid format
            pass

    def kill(self, who, args):
        if len(args) == 1:
            if self.mode == Mode.night:
                #TODO: update vote and output
                pass
            else:
                #TODO: output not valid time
                pass
        else:
            #TODO: output invalid format
            pass

    def guard(self, who, args):
        if len(args) == 1:
            if self.mode == Mode.night:
                #TODO: update vote and output
                pass
            else:
                #TODO: output not valid time
                pass
        else:
            #TODO: output invalid format
            pass

    def see(self, who, args):
        if len(args) == 1:
            if self.mode == Mode.night:
                #TODO: update vote and output
                pass
            else:
                #TODO: output not valid time
                pass
        else:
            #TODO: output invalid format
            pass

    def randplayer(self, who, args):
        if self.mode in [Mode.day_talk, Mode.day_vote]:
            tplayers = []
            for player in self.players:
                tplayers.append(player.nick)
            self.theme.user = tplayers[random.randint(0, len(tplayers)-1)]
            #TODO: print to channnel the random name

    def player_leave(self, who):
        self._rem_player(who)

    def player_nick(self, old, new):
        """player nick change"""
        self.player_leave(old)
