import asyncio
import sys
import json

async def receive_status(reader):
    """即時接收並更新顯示所有電梯的當前樓層與方向"""
    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            elevators = json.loads(data.decode().strip())
            
            # 清除當前提示行並原地更新狀態
            sys.stdout.write(f"\r" + " " * 90 + "\r")
            status_str = " | ".join([
                f"Elevator {e['id']}: {e['current_floor']:2d}F" + 
                ("^" if e['direction'] == 1 else "v" if e['direction'] == -1 else "-") 
                for e in elevators
            ])
            sys.stdout.write(f"\r[Monitor] {status_str} | Enter Call (From,To): ")
            sys.stdout.flush()
    except asyncio.CancelledError:
        pass

async def send_requests(writer):
    """發送叫車請求，格式為 '起始樓層,目的樓層'"""
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input)
        try:
            from_flr, to_flr = map(int, user_input.split(','))
            if not (1 <= from_flr <= 10 and 1 <= to_flr <= 10):
                print("\n[Error] Floors must be between 1 and 10.")
                continue
            
            req = {"from": from_flr, "to": to_flr}
            writer.write((json.dumps(req) + "\n").encode())
            await writer.drain()
        except ValueError:
            print("\n[Error] Invalid format! Please use: FromFloor,ToFloor (e.g., 3,9)")

async def main():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        print("\n[System] Successfully connected to Central Elevator Server!")
        await asyncio.gather(receive_status(reader), send_requests(writer))
    except ConnectionRefusedError:
        print("[Error] Connection refused. Is the server running?")

if __name__ == '__main__':
    asyncio.run(main())