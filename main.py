import asyncio
import random
import flet as ft

def main(page: ft.Page):
    page.title = "포켓몬 집중 타이머 & 상점 (테스트 모드)"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK 
    
    POKEMON_LIST = [
        {"id": 25, "name": "피카츄", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/25.png", "type": "popular"},
        {"id": 133, "name": "이브이", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/133.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/133.png", "type": "popular"},
        {"id": 4, "name": "파이리", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/4.png", "type": "normal"},
        {"id": 7, "name": "꼬부기", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/7.png", "type": "normal"},
        {"id": 1, "name": "이상해씨", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/1.png", "type": "normal"},
        {"id": 39, "name": "푸린", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/39.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/39.png", "type": "normal"},
        {"id": 143, "name": "잠만보", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/143.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/143.png", "type": "normal"},
        {"id": 94, "name": "팬텀", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/94.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/94.png", "type": "normal"},
        {"id": 150, "name": "뮤츠(전설)", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/150.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/150.png", "type": "legend"},
        {"id": 144, "name": "프리져(전설)", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/144.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/144.png", "type": "legend"},
        {"id": 145, "name": "썬더(전설)", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/145.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/145.png", "type": "legend"},
        {"id": 146, "name": "파이어(전설)", "image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/146.png", "shiny_image": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/146.png", "type": "legend"},
    ]

    POINT_REWARDS = {
        "normal": {"first": 100, "duplicate": 30},
        "popular": {"first": 300, "duplicate": 100},
        "legend": {"first": 1000, "duplicate": 300},
        "shiny": {"first": 3000, "duplicate": 1000}
    }

    state = {
        "seconds": 0,
        "total_seconds": 0,
        "points": 0,               
        "is_flipped": False,
        "hatched": False,
        "caught_pokemon": {},  
        "caught_shiny": {},    
        "golden_egg_active": False, 
        "has_shiny_charm": False,   
        "target_seconds": 1 
    }
    
    egg_image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png"
    golden_egg_img = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/ultra-ball.png"

    status_text = ft.Text("버튼을 눌러 테스트를 시작하세요!", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_200, text_align=ft.TextAlign.CENTER)
    timer_text = ft.Text("현재 집중 시간: 0초", size=24, weight=ft.FontWeight.W_700, color=ft.Colors.AMBER_400)
    total_timer_text = ft.Text("총 집중 시간: 0초", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_200)
    point_text = ft.Text("보유 포인트: 0 P", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_300)
    
    image_display = ft.Image(src=egg_image, width=150, height=150)

    bs_pokedex = ft.BottomSheet(content=ft.Container(padding=10), dismissible=True)
    bs_shop = ft.BottomSheet(content=ft.Container(padding=10), dismissible=True)

    def close_bs(bs):
        bs.open = False
        page.update()

    def format_time(sec):
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        if h > 0:
            return f"{h}시간 {m}분 {s}초"
        return f"{m}분 {s}초"

    def draw_pokemon(use_golden_egg=False, has_shiny_charm=False):
        popular_pokes = [p for p in POKEMON_LIST if p["type"] == "popular"]
        normal_pokes = [p for p in POKEMON_LIST if p["type"] == "normal"]
        legend_pokes = [p for p in POKEMON_LIST if p["type"] == "legend"]

        rand_val = random.uniform(0, 100)
        legend_chance = 5.0 if use_golden_egg else 1.0
        popular_chance = 50.0
        
        if rand_val < legend_chance:
            chosen = random.choice(legend_pokes)
        elif rand_val < (legend_chance + popular_chance):
            chosen = random.choice(popular_pokes)
        else:
            chosen = random.choice(normal_pokes)

        shiny_chance = 2.0 if has_shiny_charm else 0.5
        is_shiny = random.uniform(0, 100) < shiny_chance

        return chosen, is_shiny

    def open_shop(e):
        def buy_golden_egg(e):
            if state["points"] >= 1000:
                state["points"] -= 1000
                state["golden_egg_active"] = True
                image_display.src = golden_egg_img
                point_text.value = f"보유 포인트: {state['points']} P"
                status_text.value = "🌟 황금알 장착! 전설 부화 확률 5%로 상승!"
                close_bs(bs_shop)
            else:
                page.open(ft.SnackBar(ft.Text("포인트가 부족합니다! (1,000P 필요)")))
            page.update()

        def buy_candy(e):
            if state["points"] >= 50:
                state["points"] -= 50
                state["seconds"] += 1 
                point_text.value = f"보유 포인트: {state['points']} P"
                status_text.value = "🍬 이상한사탕 사용!"
                close_bs(bs_shop)
            else:
                page.open(ft.SnackBar(ft.Text("포인트가 부족합니다! (50P 필요)")))
            page.update()

        def buy_shiny_charm(e):
            if state["has_shiny_charm"]:
                page.open(ft.SnackBar(ft.Text("이미 빛나는부적을 보유하고 있습니다!")))
            elif state["points"] >= 10000:
                state["points"] -= 10000
                state["has_shiny_charm"] = True
                point_text.value = f"보유 포인트: {state['points']} P"
                status_text.value = "✨ 빛나는부적 습득! 이로치 확률 2% 상승!"
                close_bs(bs_shop)
            else:
                page.open(ft.SnackBar(ft.Text("포인트가 부족합니다! (10,000P 필요)")))
            page.update()

        charm_button_text = "보유 중" if state["has_shiny_charm"] else "구매"

        bs_shop.content = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.SHOPPING_BAG, color=ft.Colors.AMBER_300),
                            ft.Text("포켓몬 상점", size=20, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Text(f"현재 포인트: {state['points']} P", color=ft.Colors.AMBER_200, size=16),
                    ft.Divider(),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.AUTO_AWESOME, color=ft.Colors.AMBER_400),
                        title=ft.Text("황금알 (1,000 P)"),
                        subtitle=ft.Text("다음 부화 시 전설 확률 5%로 상승"),
                        trailing=ft.ElevatedButton("구매", on_click=buy_golden_egg)
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CAKE, color=ft.Colors.PINK_300),
                        title=ft.Text("이상한사탕 (50 P)"),
                        subtitle=ft.Text("시간 단축 효과"),
                        trailing=ft.ElevatedButton("구매", on_click=buy_candy)
                    ),
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.AUTO_FIX_HIGH, color=ft.Colors.PURPLE_300),
                        title=ft.Text("✨ 빛나는부적 (10,000 P)"),
                        subtitle=ft.Text("이로치 확률 2%로 상승"),
                        trailing=ft.ElevatedButton(charm_button_text, on_click=buy_shiny_charm, disabled=state["has_shiny_charm"])
                    ),
                    ft.Container(height=10),
                    ft.ElevatedButton("닫기", on_click=lambda e: close_bs(bs_shop), icon=ft.Icons.CLOSE)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            height=480
        )
        bs_shop.open = True
        page.update()

    def open_pokedex(e):
        grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=110,
            child_aspect_ratio=0.8,
            spacing=10,
            run_spacing=10,
        )
        
        for poke in POKEMON_LIST:
            poke_id = poke["id"]
            normal_cnt = state["caught_pokemon"].get(poke_id, 0)
            shiny_cnt = state["caught_shiny"].get(poke_id, 0)
            
            is_caught = normal_cnt > 0
            is_shiny_caught = shiny_cnt > 0
            is_legend = poke["type"] == "legend"
            
            if is_shiny_caught:
                img_url = poke["shiny_image"]
                display_name = f"✨{poke['name']}"
                name_color = ft.Colors.PINK_300
                count_str = f"x{shiny_cnt}"
            elif is_caught:
                img_url = poke["image"]
                display_name = poke["name"]
                name_color = ft.Colors.AMBER_200 if is_legend else ft.Colors.WHITE
                count_str = f"x{normal_cnt}"
            else:
                img_url = poke["image"]
                display_name = "???"
                name_color = ft.Colors.GREY_600
                count_str = ""

            card = ft.Container(
                content=ft.Column(
                    [
                        ft.Image(
                            src=img_url,
                            width=55,
                            height=55,
                            color=None if (is_caught or is_shiny_caught) else ft.Colors.BLACK87,
                            color_blend_mode=None if (is_caught or is_shiny_caught) else ft.BlendMode.SRC_IN
                        ),
                        ft.Text(
                            display_name,
                            size=10,
                            weight=ft.FontWeight.BOLD,
                            color=name_color,
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            count_str,
                            size=9,
                            color=ft.Colors.GREY_400,
                            text_align=ft.TextAlign.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST if (is_caught or is_shiny_caught) else ft.Colors.BLACK26,
                border_radius=10,
                padding=5
            )
            grid.controls.append(card)

        total_collected = len(set(state['caught_pokemon'].keys()).union(set(state['caught_shiny'].keys())))

        bs_pokedex.content = ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.BOOK, color=ft.Colors.AMBER_300),
                            ft.Text(f"포켓몬 도감 ({total_collected}/{len(POKEMON_LIST)})", size=18, weight=ft.FontWeight.BOLD),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Divider(),
                    ft.Container(content=grid, height=300),
                    ft.ElevatedButton("닫기", on_click=lambda e: close_bs(bs_pokedex), icon=ft.Icons.CLOSE)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            height=450
        )
        bs_pokedex.open = True
        page.update()

    def toggle_flip_test(e):
        if not state["is_flipped"]:
            state["is_flipped"] = True
            state["hatched"] = False 
            status_text.value = "🔒 테스트 모드 작동 중! (메뉴 잠김)"
            status_text.color = ft.Colors.BLUE_400
            test_flip_button.text = "중단하기"
            test_flip_button.icon = ft.Icons.LOCK_OPEN
            
            pokedex_button.disabled = True
            shop_button.disabled = True
        else:
            state["is_flipped"] = False
            status_text.value = "⚠️ 중단되었습니다."
            status_text.color = ft.Colors.ORANGE_400
            test_flip_button.text = "테스트 시작"
            test_flip_button.icon = ft.Icons.LOCK
            
            pokedex_button.disabled = False
            shop_button.disabled = False
            
        page.update()

    test_flip_button = ft.OutlinedButton(
        "테스트 시작", 
        on_click=toggle_flip_test,
        icon=ft.Icons.LOCK
    )

    shop_button = ft.ElevatedButton(
        "상점 열기", 
        on_click=open_shop, 
        icon=ft.Icons.SHOPPING_CART,
        style=ft.ButtonStyle(color=ft.Colors.GREEN_300)
    )

    pokedex_button = ft.ElevatedButton(
        "포켓몬 도감 열기", 
        on_click=open_pokedex, 
        icon=ft.Icons.CATCHING_POKEMON,
        style=ft.ButtonStyle(color=ft.Colors.AMBER_300)
    )

    async def count_timer():
        while True:
            if state["is_flipped"]:
                state["seconds"] += 1
                state["total_seconds"] += 1
                
                timer_text.value = f"현재 집중 시간: {state['seconds']}초"
                total_timer_text.value = f"총 집중 시간: {format_time(state['total_seconds'])}"
                point_text.value = f"보유 포인트: {state['points']} P"
                
                if state["seconds"] >= state["target_seconds"]:
                    target, is_shiny = draw_pokemon(
                        use_golden_egg=state["golden_egg_active"], 
                        has_shiny_charm=state["has_shiny_charm"]
                    )
                    state["golden_egg_active"] = False 
                    
                    poke_id = target["id"]
                    poke_type = "shiny" if is_shiny else target["type"]
                    
                    if is_shiny:
                        current_count = state["caught_shiny"].get(poke_id, 0)
                        state["caught_shiny"][poke_id] = current_count + 1
                        is_first = (current_count == 0)
                        image_display.src = target["shiny_image"]
                    else:
                        current_count = state["caught_pokemon"].get(poke_id, 0)
                        state["caught_pokemon"][poke_id] = current_count + 1
                        is_first = (current_count == 0)
                        image_display.src = target["image"]
                    
                    earned_points = POINT_REWARDS[poke_type]["first"] if is_first else POINT_REWARDS[poke_type]["duplicate"]
                    state["points"] += earned_points
                    
                    reward_msg = f"+{earned_points}P 획득!"
                    if is_shiny:
                        status_text.value = f"✨ 초희귀 이로치 [{target['name']}] 부화! {reward_msg}"
                        status_text.color = ft.Colors.PINK_300
                    elif target["type"] == "legend":
                        status_text.value = f"🌟 전설의 포켓몬 [{target['name']}] 부화! {reward_msg}"
                        status_text.color = ft.Colors.AMBER_300
                    else:
                        status_text.value = f"🎉 [{target['name']}] 부화 완료! {reward_msg}"
                        status_text.color = ft.Colors.GREEN_400
                    
                    state["seconds"] = 0
                
                page.update()
            await asyncio.sleep(1)

    page.overlay.append(bs_pokedex)
    page.overlay.append(bs_shop)

    page.add(
        status_text,
        ft.Container(height=5),
        point_text,
        total_timer_text,
        ft.Container(height=10),
        image_display,
        ft.Container(height=10),
        timer_text,    
        ft.Container(height=15),
        ft.Row([pokedex_button, shop_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=10),
        test_flip_button
    )

    page.run_task(count_timer)

ft.app(target=main, assets_dir="assets")