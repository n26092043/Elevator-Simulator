import unittest
import asyncio
from elevator_basic import Elevator
from elevator_advanced import AdvancedElevator, Dispatcher

class TestElevatorSystem(unittest.TestCase):

    def test_basic_elevator_initial_state(self):
        """測試基本電梯初始屬性是否符合需求"""
        e = Elevator(elevator_id=1, current_floor=1)
        self.assertEqual(e.current_floor, 1)
        self.assertFalse(e.is_moving)

    def test_smart_dispatch_nearest_idle(self):
        """測試智慧調度：當所有電梯閒置時，應分派距離最近的一台"""
        e1 = AdvancedElevator(elevator_id=1, current_floor=1)
        e2 = AdvancedElevator(elevator_id=2, current_floor=6)
        dispatcher = Dispatcher([e1, e2])

        # 有人在 2 樓叫車，離 e1(1F) 最近
        chosen = dispatcher.find_best_elevator(from_floor=2, to_floor=5)
        self.assertEqual(chosen.id, 1)

        # 有人在 7 樓叫車，離 e2(6F) 最近
        chosen = dispatcher.find_best_elevator(from_floor=7, to_floor=10)
        self.assertEqual(chosen.id, 2)

    def test_basic_elevator_movement(self):
        """測試基本電梯執行move方法後是否確實抵達目標"""
        e = Elevator(elevator_id=1, current_floor=1)
        
        async def run_test():
            await e.move(1, 4) # 從 1 樓移動到 4 樓
            
        asyncio.run(run_test())
        self.assertEqual(e.current_floor, 4)
        self.assertEqual(e.direction, 0)

if __name__ == '__main__':
    unittest.main()