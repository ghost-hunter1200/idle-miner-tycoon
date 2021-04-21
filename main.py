import pygame
import colorspy

pygame.init()


class Manager:
    def __init__(self, cost, m_type, index):
        self.level = 1
        self.type = m_type
        self.cost = cost
        self.offset = 300
        self.buffer = 10
        self.width = 500
        self.height = 100
        self.index = index
        self.x = 100
        self.y = self.offset + (self.height + self.buffer) * (self.index - 1)
        self.equiped = False
        self.btn_text = "Equip"
        self.text_color = colorspy.black

        self.equip_btn = Button(self.x + 350, self.y + 10, 100, 80, None, text_size=32)

        self.miner_img = pygame.image.load("assets/miner_employee.png").convert_alpha()
        self.seller_img = pygame.image.load("assets/seller_employee.png").convert_alpha()
        self.miner_icon = pygame.transform.scale(self.miner_img, (24, 90))
        self.seller_icon = pygame.transform.scale(self.seller_img, (24, 90))

    def draw(self):
        pygame.draw.rect(win, colorspy.lime_green, (self.x, self.y, self.width, self.height))

        if self.type == "Miner":
            win.blit(self.miner_icon, (self.x + 40, self.y + 5))
            draw_text(medium_font, self.type, (self.x + 160, self.y + 50), colorspy.blue)
        else:
            win.blit(self.seller_icon, (self.x + 40, self.y + 5))
            draw_text(medium_font, self.type, (self.x + 160, self.y + 50), colorspy.dark_green)

        self.equip_btn.draw()
        draw_text(medium_font, self.btn_text, (self.x + 400, self.y + 50), self.text_color)

        draw_text(font, f"Level: {self.level}", (self.x + 250, self.y + 50), colorspy.black)


class Mine:
    def __init__(self, mine_no):
        self.mine_no = mine_no
        self.level = 1
        self.miners = 1
        self.worker_capacity = 400 * (10 ** (self.mine_no - 1))
        self.upgrade_cost = 100
        self.manager_owned = False
        self.equiped_manager = None

        self.width = 450
        self.height = 150
        self.offset = 200
        self.buffer = 20
        self.x = 120
        self.y = self.offset + (self.height + self.buffer) * (self.mine_no - 1)
        self.storage = 0
        self.frame = 0
        self.frameCount = 0
        self.frameDir = 1
        self.mining = False
        self.selected_button = "x1"

        # Buttons
        self.buttons = [Button(WIDTH - 120, self.y + 10, 60, 70, self.mine, "Mine!", text_size=24),
                        Button(WIDTH - 120, self.y + 90, 60, 50, self.upgrade_screen, "Upgrade", text_size=20),
                        Button(self.x + 10, self.y + 10, 60, 70, self.sell, text_size=24),
                        Button(self.x + 10, self.y + 90, 60, 50, self.work, text_size=20)]

        # Images
        self.coal_img = pygame.transform.scale(pygame.image.load('assets/coal.png').convert_alpha(), (150, 150))
        self.metal_img = pygame.transform.scale(pygame.image.load('assets/metal.png').convert_alpha(), (180, 150))
        self.miner_imgs = [pygame.transform.scale(pygame.image.load('assets/miner.png').convert_alpha(), (68, 96)),
                           pygame.transform.scale(pygame.image.load('assets/miner2.png').convert_alpha(), (68, 96)),
                           pygame.transform.scale(pygame.image.load('assets/miner3.png').convert_alpha(), (68, 96))]
        self.back_arrow = pygame.transform.scale(pygame.image.load('assets/arrow.png').convert_alpha(), (64, 64))
        self.back_arrow.set_colorkey(colorspy.white)

    def draw(self):
        pygame.draw.rect(win, (187, 81, 57), (self.x, self.y + y, self.width, self.height))
        win.blit(self.coal_img, (WIDTH - 150, self.y + y))
        win.blit(self.coal_img, (self.x, self.y + y))
        pygame.draw.rect(win, colorspy.white, (10, self.y + y + 25, 100, 100), border_radius=8)
        draw_text(big_font, str(self.mine_no), (60, self.y + y + 60), colorspy.black)
        draw_text(font, "Level " + str(self.level), (60, self.y + y + 90), colorspy.black)

        for i in range(self.miners):
            win.blit(self.miner_imgs[self.frame], (WIDTH - 220 + i * 10, self.y + (150 - 96) + y))

        self.animate()

        for button in self.buttons:
            button.draw()

        if not self.manager_owned:
            draw_text(small_font, "Equip", (self.x + 40, self.y + 110 + y), colorspy.black)
        else:
            draw_text(small_font, "Upgrade", (self.x + 40, self.y + 105 + y), colorspy.black)
        draw_text(small_font, "Worker", (self.x + 40, self.y + 125 + y), colorspy.black)

        draw_text(small_font, "Sell!", (self.x + 40, self.y + 35 + y), colorspy.black)
        draw_text(small_font, number(self.storage), (self.x + 40, self.y + 60 + y), colorspy.black)

    def mine(self):
        self.mining = True

    def mine_finished(self):
        self.storage += self.worker_capacity * self.miners

    def upgrade(self):
        global coins
        if coins >= self.upgrade_cost and self.level < 800:
            self.level += 1
            coins -= self.upgrade_cost

            if self.level in (25, 100, 300, 400, 600, 700):
                self.worker_capacity = round(2.5 * self.worker_capacity)
            else:
                if self.level in (10, 50, 200, 500, 800):
                    self.miners += 1

                self.worker_capacity = round(1.1 * self.worker_capacity)

            self.upgrade_cost = round(1.5 * self.upgrade_cost)

    def upgrade_screen(self):
        global coins, run
        win = pygame.display.set_mode((700, 1000))
        running = True
        buttons = [Button(10, 890, 100, 100, None, "x1", hovered_color=colorspy.off_white, scrolling=False),
                   Button(120, 890, 100, 100, None, "x10", hovered_color=colorspy.off_white, scrolling=False),
                   Button(230, 890, 100, 100, None, "x50", hovered_color=colorspy.off_white, scrolling=False),
                   Button(340, 890, 100, 100, None, "Max", hovered_color=colorspy.off_white, scrolling=False),
                   Button(490, 890, 200, 100, None, "UPGRADE", scrolling=False)]
        for button in buttons:
            if self.selected_button == button.text:
                button.bg_color = colorspy.off_white
                button.fg_color = colorspy.off_white
                button.old_bg_color = colorspy.off_white
                break

        upgrades, upgrade_cost = self.upgrade_x(self.selected_button[1:])
        level, worker_capacity, miners = self.level, self.worker_capacity, self.miners

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                    run = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if e.button == 1:
                        if 50 < mouse_x < 64 + 50 and 50 < mouse_y < 64 + 50:
                            running = False

                        for button in buttons:
                            if button.mouse_hovered():

                                if button.text != "UPGRADE":

                                    if self.level != 800:
                                        button.old_bg_color = colorspy.off_white
                                        button.bg_color = colorspy.off_white
                                        self.selected_button = button.text
                                        upgrades, upgrade_cost = self.upgrade_x(self.selected_button[1:])

                                        level, worker_capacity, miners = self.level, self.worker_capacity, self.miners

                                        for i in range(upgrades):

                                            if level + 1 in (25, 100, 300, 400, 600, 700):
                                                worker_capacity = round(2.5 * worker_capacity)
                                            else:
                                                worker_capacity = round(1.1 * worker_capacity)
                                                if level + 1 in (10, 50, 200, 500, 800):
                                                    miners += 1

                                            level += 1

                                else:

                                    if coins >= upgrade_cost:
                                        for i in range(upgrades):
                                            self.upgrade()

                                    upgrades, upgrade_cost = self.upgrade_x(self.selected_button[1:])
                                    level, worker_capacity, miners = self.level, self.worker_capacity, self.miners

                                    for i in range(upgrades):
                                        if level + 1 in (25, 100, 300, 400, 600, 700):
                                            worker_capacity = round(2.5 * worker_capacity)
                                        else:
                                            worker_capacity = round(1.1 * worker_capacity)
                                            if level + 1 in (10, 50, 200, 500, 800):
                                                miners += 1
                                        level += 1
                            else:
                                for button_ in buttons:
                                    if button_.text != self.selected_button:
                                        button_.bg_color = colorspy.white
                                        button_.old_bg_color = colorspy.white

            win.fill((179, 185, 136))

            pygame.draw.rect(win, (152, 194, 245), (50, 150, 600, 700), border_radius=25)

            draw_text(font, f"x{upgrades}, cost: {number(upgrade_cost)}", (590, 870), colorspy.black)

            draw_text(big_font, "Mine {} - Level {}".format(self.mine_no, self.level), (350, 180), colorspy.black)
            draw_text(font, "Next boost at level " + str(
                min([i for i in (10, 25, 50, 100, 200, 300, 400, 500, 600, 700, 800) if i >= self.level])), (350, 240),
                      colorspy.black)

            draw_text(big_font, f"Total extraction:  {str(number(self.worker_capacity * self.miners))}/s", (350, 350), colorspy.black)
            draw_text(medium_font, f"+{str(number(worker_capacity * miners - self.worker_capacity * self.miners))}", (350, 380), colorspy.green)
            draw_text(big_font, f"Miners:  {str(self.miners )}", (350, 450), colorspy.black)
            draw_text(medium_font, f"+{str(miners - self.miners)}", (350, 480), colorspy.green)

            if self.level < 800:
                for button in buttons:
                    button.draw()

            else:
                draw_text(big_font, "MAX UPGRADED", (350, 900), colorspy.red)

            draw_text(big_font, f"{number(coins)}", (350, 30), colorspy.black)

            win.blit(self.back_arrow, (50, 50))

            pygame.display.update()

    def upgrade_x(self, num):
        global coins
        total_cost = 0
        upgrade_cost = self.upgrade_cost

        if num != "ax":
            for i in range(int(num)):
                total_cost += upgrade_cost
                upgrade_cost = round(upgrade_cost * 1.5)
            return int(num), total_cost

        else:
            upgrades = 0
            while coins >= total_cost + upgrade_cost:
                upgrade_cost = round(upgrade_cost * 1.5)
                total_cost += upgrade_cost
                upgrades += 1

                if self.level + upgrades > 800:
                    upgrades = 800 - self.level

            return upgrades, total_cost

    def sell(self):
        global coins
        coins += self.storage
        self.storage = 0

    def work(self):
        global coins, managers, run, new_manager_cost
        win = pygame.display.set_mode((700, 1000))

        running = True
        while running:
            for e in pygame.event.get():

                if e.type == pygame.QUIT:
                    run = running = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if e.button == 1:
                        if 50 < mouse_x < 64 + 50 and 50 < mouse_y < 64 + 50:
                            running = False

                        for manager in managers:
                            if manager.equip_btn.mouse_hovered() and not manager.equiped:
                                manager.equiped = True
                                manager.btn_text = "Equiped"
                                manager.text_color = colorspy.red
                                self.manager_owned = True
                                self.equiped_manager = manager
                                manager_index = managers.index(manager)

                                for m in managers:
                                    if not managers.index(m) == manager_index:
                                        m.equiped = False
                                        m.btn_text = "Equip"
                                        m.text_color = colorspy.black

            win.fill((179, 185, 136))

            pygame.draw.rect(win, (152, 194, 245), (50, 150, 600, 700), border_radius=25)

            for manager in managers:
                manager.draw()

            draw_text(big_font, f"{number(coins)}", (350, 30), colorspy.black)

            win.blit(self.back_arrow, (50, 50))

            pygame.display.update()

    def animate(self):
        if self.mining:
            self.frameCount += 1
            if self.frameCount <= 60:
                if self.frameCount % 5 == 0:
                    self.frame += self.frameDir
                    if self.frame == 2:
                        self.frameDir = -1
                    elif self.frame == 0:
                        self.frameDir = 1
            else:
                self.frameCount = 0
                self.frameDir = 1
                self.mining = False
                self.mine_finished()


class Button:
    def __init__(self, x, y, w, h, function, text=None, bg_color=colorspy.white, fg_color=colorspy.black,
                 hovered_color=None,
                 text_color=colorspy.black, text_size=None, font='comicsans', border_size=0, image=None, scrolling=True):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.scrolling = scrolling
        self.function = function
        self.text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.old_bg_color = bg_color
        self.old_fg_color = fg_color
        self.text_color = text_color
        self.font = font
        self.b_size = border_size
        self.img = image

        if text_size is None:
            self.text_font = pygame.font.SysFont(font, round(self.h * 0.50))
        else:
            self.text_font = pygame.font.SysFont(font, text_size)

        if not hovered_color:
            self.hovered_color = self.bg_color
        else:
            self.hovered_color = hovered_color

    def draw(self):
        if self.scrolling:
            if self.b_size > 0:
                pygame.draw.rect(win, self.fg_color, (
                self.x - self.b_size, self.y - self.b_size + y, self.w + self.b_size * 2, self.h + self.b_size * 2),
                                 self.b_size, border_radius=15)

            pygame.draw.rect(win, self.bg_color, (self.x, self.y + y, self.w, self.h))
        else:
            if self.b_size > 0:
                pygame.draw.rect(win, self.fg_color, (
                    self.x - self.b_size, self.y - self.b_size, self.w + self.b_size * 2, self.h + self.b_size * 2),
                                 self.b_size)

            pygame.draw.rect(win, self.bg_color, (self.x, self.y, self.w, self.h))

        if self.mouse_hovered():
            self.bg_color = self.hovered_color

        else:
            self.bg_color = self.old_bg_color

        self.draw_text()

        if not self.img is None:
            self.draw_image()

    def mouse_hovered(self):
        xPos, yPos = pygame.mouse.get_pos()
        if self.scrolling:
            if self.x <= xPos <= self.x + self.w and self.y + y <= yPos <= self.y + y + self.h:
                return True

            return False
        else:
            if self.x <= xPos <= self.x + self.w and self.y <= yPos <= self.y + self.h:
                return True

            return False

    def draw_text(self):
        text = self.text_font.render(self.text, True, self.text_color)
        if self.scrolling:
            win.blit(text, (self.x + (self.w / 2) - text.get_width() / 2, y + self.y + (self.h / 2) - text.get_height() / 2))
        else:
            win.blit(text, (self.x + (self.w / 2) - text.get_width() / 2, self.y + (self.h / 2) - text.get_height() / 2))

    def draw_image(self):
        img_rect = pygame.Rect(self.x + (self.w / 2) - self.img.get_width() / 2,
                               self.y + (self.h / 2) - self.img.get_height() / 2 + y, self.img.get_width(),
                               self.img.get_height())
        win.blit(self.img, img_rect)


SCREEN_SIZE = WIDTH, HEIGHT = 700, 1000
win = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Idle Miner Tycoon")
clock = pygame.time.Clock()

# Fonts
small_font = pygame.font.SysFont('comicsans', 20)
font = pygame.font.SysFont('comicsans', 24)
medium_font = pygame.font.SysFont('comicsans', 32)
big_font = pygame.font.SysFont('comicsans', 48)


def draw_text(font, text, center_pos, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = center_pos
    win.blit(text_surface, text_rect)


def number(num):
    endings = ["K", "M", "B", "T", "aa", "ab", "ac", "ad", "ae", "af", "ag", "ah", "ai", "aj", "ak", "al", "am", "an",
               "ao", "ap", "aq", "ar", "as", "at", "au", "av", "aw", "ax", "ay", "az"]

    if num < 1000:
        return str(num)

    elif num > 1000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000:
        for i in range(30):
            num /= 1000

        return str(round(num, 2)) + " " + endings[-1]

    i = 0
    while num >= 1000:
        num /= 1000
        i += 1

    return str(round(num, 2)) + " " + endings[i - 1]


def hire_manager():
    global run, coins, new_manager_cost
    win = pygame.display.set_mode((700, 1000))

    buttons = [Button(230, 400, 250, 150, None, text_size=32, scrolling=False),
               Button(230, 600, 250, 150, None, text_size=32, scrolling=False)]
    text = ["Hire Miner", "Hire Seller", number(new_manager_cost), number(new_manager_cost)]

    back_arrow = pygame.transform.scale(pygame.image.load('assets/arrow.png').convert_alpha(), (64, 64))
    back_arrow.set_colorkey(colorspy.white)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if event.button == 1:
                    if 50 < mouse_x < 64 + 50 and 50 < mouse_y < 64 + 50:
                        running = False
                    for button in buttons:
                        if button.mouse_hovered():
                            if coins >= new_manager_cost:
                                coins -= new_manager_cost
                                managers.append(Manager(new_manager_cost, text[buttons.index(button)][5:], len(managers)))
                                new_manager_cost *= 20
                                text[2] = text[3] = number(new_manager_cost)

        win.fill((179, 185, 136))

        for button in buttons:
            button.draw()

        draw_text(big_font, number(coins), (WIDTH / 2, 30), colorspy.black)

        draw_text(medium_font, text[0], (350, 450), colorspy.black)
        draw_text(medium_font, text[2], (350, 500), colorspy.black)

        draw_text(medium_font, text[1], (350, 650), colorspy.black)
        draw_text(medium_font, text[3], (350, 700), colorspy.black)

        draw_text(big_font, f"Managers Owned: {len(managers)}", (350, 200), colorspy.black)

        win.blit(back_arrow, (50, 50))
        pygame.display.update()


mines = [Mine(1)]
coins = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

new_mine_btn = Button(WIDTH - 120, 370, 100, 70, None, "New Mine", text_size=26)
new_mine_cost = 500000
new_mine_cost_height = 420

hire_manager_btn = Button(20, 370, 100, 70, hire_manager, text_size=20)
manager_height = 400
managers = []
new_manager_cost = 100000

y = 0
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(mines) > 4:
                if event.button == 5:
                    y -= 20
                elif event.button == 4:
                    y += 20
            if y > 0:
                y = 0
            elif y < -4400:
                y = -4400

            if event.button == 1:
                for mine in mines:
                    for button in mine.buttons:
                        if button.mouse_hovered():
                            button.function()
                if hire_manager_btn.mouse_hovered():
                    hire_manager_btn.function()

                if new_mine_btn.mouse_hovered() and len(mines) < 30 and coins > new_mine_cost:
                    coins -= new_mine_cost
                    mines.append(Mine(len(mines) + 1))
                    new_mine_btn.y += 170
                    new_mine_cost *= 20
                    new_mine_cost_height += 170
                    hire_manager_btn.y += 170
                    manager_height += 170

    win.fill((179, 185, 136))

    for mine in mines:
        mine.draw()

    if len(mines) < 30:
        new_mine_btn.draw()
        draw_text(font, number(new_mine_cost), (WIDTH - 70, new_mine_cost_height + y), colorspy.black)

    hire_manager_btn.draw()
    draw_text(font, "Hire", (70, manager_height + y), colorspy.black)
    draw_text(font, "Manager", (70, manager_height + 20 + y), colorspy.black)

    draw_text(big_font, number(coins), (WIDTH / 2, 30), colorspy.black)

    pygame.display.update()

pygame.quit()