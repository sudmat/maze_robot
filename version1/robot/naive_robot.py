class NaiveRobot:

    def next_move(self, cur_state):
        if not cur_state['state'] == 2:
            return 'RIGHT'
        return 'STAY'
