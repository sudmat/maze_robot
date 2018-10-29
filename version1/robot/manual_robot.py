class ManualRobot:

    def next_move(self, cur_state):
        for k in ['RIGHT', 'LEFT', 'UP', 'DOWN']:
            if cur_state['input'][k]:
                return k
        return 'STAY'
