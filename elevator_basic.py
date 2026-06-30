import asyncio
import sys

class Elevator:
    def __init__(self, elevator_id: int, current_floor: int = 1):
        self.id = elevator_id
        self.current_floor = current_floor
        self.is_moving = False
        self.direction = 0  # 0: Idle, 1: Up, -1: Down

    def display_floor(self):
        """顯示目前樓層 (題目要求方法)"""
        status = "IDLE" if self.direction == 0 else ("UP" if self.direction == 1 else "DOWN")
        print(f"[Elevator {self.id}] Current Floor: {self.current_floor:2d} | Status: {status}")

    async def move(self, current: int, floor: int):
        """移動電梯至指定樓層 (題目要求方法)"""
        # 如果電梯目前不在乘客所在樓層(current)，先去接人
        if self.current_floor != current:
            print(f"\n[System] Elevator {self.id} moving to pick up passenger at floor {current}...")
            await self._travel_to(current)
            print(f"[System] Elevator {self.id} arrived at pickup floor {current}. Door opening...")
            await asyncio.sleep(1) # 停等乘客上車
        
        # 前往目的地 (floor)
        print(f"\n[System] Elevator {self.id} moving to destination floor {floor}...")
        await self._travel_to(floor)
        print(f"★ [System] Elevator {self.id} safely arrived at destination floor {self.current_floor}!\n")

    async def _travel_to(self, target: int):
        """內部核心移動邏輯，模擬每層樓 1 秒"""
        if target == self.current_floor:
            self.direction = 0
            self.display_floor()
            return

        self.is_moving = True
        self.direction = 1 if target > self.current_floor else -1

        while self.current_floor != target:
            await asyncio.sleep(1)  # 加分項 1: 每層樓移動花費 1 秒
            self.current_floor += self.direction
            self.display_floor()

        self.is_moving = False
        self.direction = 0


async def user_interface(elevators):
    """手動輸入的文字操作介面"""
    loop = asyncio.get_event_loop()
    
    print("==============================================")
    print("        Elevator Simulator (Basic Version)    ")
    print("==============================================")
    print("Instruction: Enter command as 'ElevatorID,CurrentFloor,TargetFloor'")
    print("Example: '1,2,7' means Elevator 1 picks up at 2F and goes to 7F.")
    print("Type 'exit' to quit.")
    print("==============================================")

    while True:
        # 顯示目前兩台電梯的位置
        print("\n[Current Positions] ", end="")
        for e in elevators.values():
            print(f"Elevator {e.id}: {e.current_floor}F  ", end="")
        print()
        
        print("Enter command: ", end="")
        # 使用 run_in_executor 避免 input() 卡死 asyncio 事件循環
        user_input = await loop.run_in_executor(None, sys.stdin.readline)
        user_input = user_input.strip()

        if user_input.lower() == 'exit':
            print("[System] Exiting system...")
            break

        try:
            e_id, current_flr, target_flr = map(int, user_input.split(','))
            
            if e_id not in elevators:
                print(f"[Error] Invalid Elevator ID {e_id}. Available: {list(elevators.keys())}")
                continue
            
            if not (1 <= current_flr <= 10 and 1 <= target_flr <= 10):
                print("[Error] Floor numbers must be between 1 and 10.")
                continue

            elevator = elevators[e_id]
            
            if elevator.is_moving:
                print(f"[Warning] Elevator {e_id} is currently busy! Request ignored. Please wait.")
                continue
            
            # 使用 asyncio.create_task 實現非同步並行，指令送出後立刻進入下一次迴圈接受新輸入
            asyncio.create_task(elevator.move(current_flr, target_flr))

        except ValueError:
            print("[Error] Invalid format! Please use: ElevatorID,CurrentFloor,TargetFloor (e.g., 1,1,5)")

async def main():
    # 建立兩台電梯，初始在 1 樓
    elevator1 = Elevator(elevator_id=1, current_floor=1)
    elevator2 = Elevator(elevator_id=2, current_floor=1)
    elevators = {1: elevator1, 2: elevator2}
    
    await user_interface(elevators)

if __name__ == '__main__':
    asyncio.run(main())