import asyncio
import json

class AdvancedElevator:
    def __init__(self, elevator_id: int, current_floor: int = 1):
        self.id = elevator_id
        self.current_floor = current_floor
        self.target_floor = current_floor
        self.is_moving = False
        self.direction = 0  # 0: Idle, 1: Up, -1: Down

    async def move_to(self, destination: int):
        if destination == self.current_floor:
            self.direction = 0
            return

        self.target_floor = destination
        self.is_moving = True
        self.direction = 1 if destination > self.current_floor else -1

        while self.current_floor != destination:
            await asyncio.sleep(1)  # 每層樓 1 秒
            self.current_floor += self.direction
            print(f"[Server Status] Elevator {self.id} is at {self.current_floor}F")

        self.is_moving = False
        self.direction = 0


class Dispatcher:
    """高級加分項：智慧調度演算法 (最小化乘客等待時間)"""
    def __init__(self, elevators):
        self.elevators = elevators

    def find_best_elevator(self, from_floor: int, to_floor: int) -> AdvancedElevator:
        best_elevator = None
        min_cost = float('inf')
        requested_dir = 1 if to_floor > from_floor else -1

        for env in self.elevators:
            cost = 0
            if not env.is_moving:
                # 閒置電梯：代價就是純粹距離
                cost = abs(env.current_floor - from_floor)
            else:
                if env.direction == requested_dir:
                    # 同向且尚未錯過該樓層
                    if (env.direction == 1 and env.current_floor <= from_floor) or \
                       (env.direction == -1 and env.current_floor >= from_floor):
                        cost = abs(env.current_floor - from_floor)
                    else:
                        # 同向但已錯過
                        cost = abs(env.target_floor - env.current_floor) + abs(env.target_floor - from_floor)
                else:
                    # 反向
                    cost = abs(env.target_floor - env.current_floor) + abs(env.target_floor - from_floor)

            if cost < min_cost:
                min_cost = cost
                best_elevator = env
        
        return best_elevator


class ElevatorServer:
    def __init__(self, num_elevators=3, host='127.0.0.1', port=8888):
        # 支援配置 N 台電梯
        self.elevators = [AdvancedElevator(i+1) for i in range(num_elevators)]
        self.dispatcher = Dispatcher(self.elevators)
        self.host = host
        self.port = port
        self.clients = set()

    async def broadcast_status(self):
        """廣播 JSON 狀態給所有連線的 Client 監控端"""
        while True:
            if self.clients:
                status_data = [
                    {
                        "id": e.id,
                        "current_floor": e.current_floor,
                        "target_floor": e.target_floor,
                        "is_moving": e.is_moving,
                        "direction": e.direction
                    } for e in self.elevators
                ]
                message = json.dumps(status_data) + "\n"
                for writer in list(self.clients):
                    try:
                        writer.write(message.encode())
                        await writer.drain()
                    except:
                        self.clients.remove(writer)
            await asyncio.sleep(0.5)

    async def handle_client(self, reader, writer):
        self.clients.add(writer)
        print(f"\n[Server] New Client Connected.")
        try:
            while True:
                data = await reader.readline()
                if not data:
                    break
                
                req = json.loads(data.decode().strip())
                from_flr = req['from']
                to_flr = req['to']
                
                print(f"\n[Request] Call from {from_flr}F to {to_flr}F")
                
                # 自動調度最優電梯
                chosen_elevator = self.dispatcher.find_best_elevator(from_flr, to_flr)
                print(f"[Dispatch] Assigned Elevator {chosen_elevator.id}")
                
                asyncio.create_task(self.run_job(chosen_elevator, from_flr, to_flr))
        except:
            pass
        finally:
            self.clients.remove(writer)
            writer.close()

    async def run_job(self, elevator, from_floor, to_floor):
        await elevator.move_to(from_floor)
        await elevator.move_to(to_floor)

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"=== Elevator Central Server Started ===")
        print(f"Listening on {self.host}:{self.port} | Total Elevators: {len(self.elevators)}")
        await asyncio.gather(server.serve_forever(), self.broadcast_status())

if __name__ == '__main__':
    # 可自由修改 N 台電梯數量以展現加分效果
    server = ElevatorServer(num_elevators=3)
    asyncio.run(server.start())