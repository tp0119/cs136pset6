#!/usr/bin/env python

import sys

from gsp import GSP
from util import argmax_index

class Graashoppersbudget:
    """Balanced bidding agent"""
    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget
        self.bids = []

    def initial_bid(self, reserve):
        bid = self.value / 2
        self.bids.append(bid)
        return bid


    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        prev_round = history.round(t-1)
        other_bids = [a_id_b for a_id_b in prev_round.bids if a_id_b[0] != self.id]

        clicks = prev_round.clicks
        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)
            
        info = list(map(compute, list(range(len(clicks)))))
#        sys.stdout.write("slot info: %s\n" % info)
        return info


    def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        returns a list of utilities per slot.
        """
        # TODO: Fill this in
        utilities = []   # Change this

        prev_round = history.round(t-1)
        prev_bids = prev_round.bids
        clicks = prev_round.clicks
        info = self.slot_info(t, history, reserve)
        print(info, len(info))

        for i in range(len(info)):
            # pos_i-1 * (v_i - b_i)
            exp_util = clicks[i] * (self.value - info[i][1])
            utilities.append(exp_util)
        
        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i =  argmax_index(self.expected_utils(t, history, reserve))
        info = self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
        bid = 0

        # If number of clicks is decreasing, bid less
        if t > 0 and t <= 24:
            bid = self.bids[t-1] * 0.75
            
        # If number of clicks is increasing, bid more
        elif t > 24 and t <= 48:
            bid = self.bids[t-1] * 1.75

        big = min(bid, self.value)
        self.bids.append(bid)
        return bid

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)


