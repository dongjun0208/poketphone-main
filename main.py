import flet as ft
import time
import threading
import random

def main(page: ft.Page):
    page.title = "포켓몬 집중 타이머 MVP"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK 
    
    POKEMON_LIST = [
        {"id": 25, "name": "피카츄", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"},
        {"id": 4, "name": "파이리", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png"},
        {"id": 7, "name": "꼬부기", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png"},
        {"id": 1, "name": "이상해씨", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png"},
        {"id": 133, "name": "이브이", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png"},
        {"id": 39, "name": "푸린", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png"},
        {"id": 143, "name": "잠만보", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png"},
        {"id": 94, "name": "팬텀", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png"},
    ]

    state = {
        "seconds": 0,
        "total_seconds": 0,
        "is_flipped": False,
        "hatched": False,
        "caught_pokemon": set(),
        "current_target": None
    }
    
    egg_image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"

    status_text = ft.Text("스마트폰을 뒤집어 주세요!", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200)
    timer_text = ft.Text("현재 집중 시간: 0초", size=28, weight=ft.FontWeight.W_700, color=ft.Colors.AMBER_400)
    total_timer_text = ft.Text("총 집중 시간: 0초", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_200)
    image_display = ft.Image(src=egg_image, width=160, height=160)
    
    def reset_total_time(e):
        state["total_seconds"] = 0
        total_timer_text.value = "총 집중 시간: 0초"
        print("[LOG] 사용자가 총 집중 시간을 강제로 초기화함")
        page.update()
        
    reset_button = ft.TextButton("총 집중 시간 초기화", on_click=reset_total_time, icon=ft.Icons.REFRESH)

    def open_pokedex(e):
        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=110,
            child_aspect_ratio=0.9,
            spacing=10,
            run_spacing=10,
        )
        
        for poke in POKEMON_LIST:
            is_caught = poke["id"] in state["caught_pokemon"]
            
            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=poke["image"],
                            width=60,
                            height=60,
                            color=None if is_caught else ft.Colors.BLACK54,
                            color_blend_mode=None if is_caught else ft.BlendMode.SRC_IN
                        ),
                        ft.Text(
                            poke["name"] if is_caught else "???",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE if is_caught else ft.Colors.GREY_600
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST if is_caught else ft.Colors.BLACK26,
                border_radius=10,
                padding=5
            )
            grid.controls.append(card)

        bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text(f"📖 포켓몬 도감 ({len(state['caught_pokemon'])}/{len(POKEMON_LIST)})", size=20, weight=ft.FontWeight.BOLD),
                        ft.Divider(),
                        ft.Container(content=grid, height=280),
                        ft.ElevatedButton("닫기", on_click=lambda _: page.close(bs))
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                ),
                padding=20,
                height=420
            ),
            dismissible=True
        )
        page.open(bs)

    pokedex_button = ft.ElevatedButton("📖 포켓몬 도감 열기", on_click=open_pokedex, style=ft.ButtonStyle(color=ft.Colors.AMBER_300))

    def count_timer():
        while True:
            if state["is_flipped"]:
                state["seconds"] += 1
                state["total_seconds"] += 1
                
                timer_text.value = f"현재 집중 시간: {state['seconds']}초"
                total_timer_text.value = f"총 집중 시간: {state['total_seconds']}초"
                
                if state["seconds"] >= 10 and not state["hatched"]:
                    state["hatched"] = True
                    
                    target = random.choice(POKEMON_LIST)
                    state["current_target"] = target
                    state["caught_pokemon"].add(target["id"])
                    
                    status_text.value = f"🎉 성공! [{target['name']}] 이(가) 부화했습니다!"
                    status_text.color = ft.Colors.GREEN_400
                    image_display.src = target["image"]
                
                page.update()
            time.sleep(1)

    threading.Thread(target=count_timer, daemon=True).start()

    def handle_sensor_change(e):
        try:
            z = e.z
            if z < -7.0 and not state["is_flipped"]:
                state["is_flipped"] = True
                status_text.value = "📱 폰을 뒤집었습니다. 집중 중..."
                status_text.color = ft.Colors.BLUE_400
                page.update()
                
            elif z > -4.0 and state["is_flipped"]:
                state["is_flipped"] = False
                status_text.value = "⚠️ 규칙 위반! 폰을 다시 만졌습니다."
                status_text.color = ft.Colors.RED_400
                
                state["seconds"] = 0
                state["hatched"] = False
                timer_text.value = "현재 집중 시간: 0초"
                image_display.src = egg_image
                page.update()
        except Exception as ex:
            print(f"[ERROR] 센서 처리 오류: {ex}")

    try:
        accelerometer = ft.Accelerometer()
        if hasattr(accelerometer, "on_change"):
            accelerometer.on_change = handle_sensor_change
        elif hasattr(accelerometer, "on_update"):
            accelerometer.on_update = handle_sensor_change
        
        page.overlay.append(accelerometer)
    except Exception as e:
        print(f"[WARN] 센서를 사용할 수 없습니다: {e}")

    page.add(
        status_text,
        ft.Container(height=5),
        total_timer_text,
        ft.Container(height=10),
        image_display,
        ft.Container(height=10),
        timer_text,     
        ft.Container(height=15),
        pokedex_button,
        ft.Container(height=5),
        reset_button
    )

ft.app(target=main)