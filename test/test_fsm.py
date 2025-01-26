#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# File          : test_fsm
# Author        : Sun YiFan-Movoid
# Time          : 2025/1/27 0:07
# Description   : 
"""
from movoid_fsm import FSM


class TestFsm:
    def test_01_fsm_do(self):
        FSM.add_rule('test1', ['idle', 'init', 'running', 'stopping', 'dying', 'death'],
                     [
                         [None, 'init', None, None, 'die', None, ],
                         [None, None, 'run', None, 'die', None, ],
                         [None, 'finish', None, 'stop', 'die', None, ],
                         [None, 'finish', None, None, 'die', None, ],
                         [None, None, None, None, None, 'death', ],
                         ['reborn', None, None, None, None, None, ],
                     ])
        fsm = FSM['test1']
        assert fsm.status == 'idle'
        fsm.do('init')
        assert fsm.status == 'init'
        fsm.do('die')
        assert fsm.status == 'dying'
        fsm.do('death')
        assert fsm.status == 'death'
        fsm.do('reborn')
        assert fsm.status == 'idle'
        fsm.do('init')
        assert fsm.status == 'init'
        fsm.do('run')
        assert fsm.status == 'running'
        fsm.do('finish')
        assert fsm.status == 'init'
        fsm.do('run')
        assert fsm.status == 'running'
        fsm.do('stop')
        assert fsm.status == 'stopping'
        fsm.do('finish')
        assert fsm.status == 'init'
        fsm.do('run')
        assert fsm.status == 'running'
        fsm.do('stop')
        assert fsm.status == 'stopping'
        fsm.do('die')
        assert fsm.status == 'dying'
        fsm.do('death')
        assert fsm.status == 'death'
        fsm.do('reborn')
        assert fsm.status == 'idle'
        fsm.do('init')
        assert fsm.status == 'init'
        fsm.do('run')
        assert fsm.status == 'running'
        fsm.do('die')
        assert fsm.status == 'dying'
        fsm.do('death')
        assert fsm.status == 'death'

    def test_02_fsm_when(self):
        FSM.add_rule('test2', ['init', 'running', 'death'],
                     [
                         [None, 'run', 'die', ],
                         ['finish', None, 'die', ],
                         ['init', None, None, ],
                     ])
        fsm = FSM['test2']
        fsm.check_status_now('init')

        @FSM.test2.when('init', setup_action='run', return_action='finish', exception_action='die')
        def run(error=False):
            fsm.check_status_now('running')
            if error:
                raise Exception

        run()
        fsm.check_status_now('init')
        try:
            run(True)
        except:
            fsm.check_status_now('death')
        else:
            raise AssertionError
