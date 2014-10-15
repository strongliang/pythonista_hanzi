# coding: utf-8
import ui

view = ui.load_view('hanzi')

view.width, view.height = ui.get_screen_size()

scroll = view['scrollview1']
scroll.x, scroll.y = view.x, view.y
scroll.width, scroll.height = view.width, view.height
view.add_subview(scroll)
big_button = view['button1']
scroll.add_subview(big_button)


debug = view['textview1']
debug.text = ''

# global settings
zi_w = 40  # hanzi width
zi_h = 30  # hanzi height
hor_margin = 5  # horizontal margin
ver_margin = 1  # vertical margin

zi_spacing = 5
line_spacing = 1

view_x, view_y, view_w, view_h = view.bounds

# red green blue
BLACK = (0, 0, 0, 1)
WHITE = (1, 1, 1, 1)

global_show_hide_switch = True


def show_one_zi(sender):
    yin = sender.superview['yin']
    if yin.text_color == WHITE:
        yin.text_color = BLACK
    else:
        yin.text_color = WHITE


def show_all_zi(sender):
    global global_show_hide_switch
    for elem in scroll.subviews:
        if isinstance(elem, ui.View) and elem['yin']:
            yin = elem['yin']
            if global_show_hide_switch:
                yin.text_color = BLACK
                big_button.title = 'hide'
                new_value = False
            else:
                yin.text_color = WHITE
                big_button.title = 'show'
                new_value = True

    global_show_hide_switch = new_value


# converting pinyin and charaters into lists are tricky
# notice the placement of spaces in the pinyin string
def display_data():
    # han = '我是一个粉刷匠，粉刷本领强。'
    # pin = 'Wǒ shì yī gè fěn shuā jiàng ， fěn shuā běn lǐng qiáng 。'
    han = '则需要满足技术指标才能获得资金，而且签订的协议阻止公司向其他公司供应蓝宝石材料。' * 5
    pin = 'zé xū yào mǎn zú jì shù zhǐ biāo cái néng huò dé zī jīn ， ér qiě qiān dìng de xié yì zǔ zhǐ gōng sī xiàng qí tā gōng sī gōng yìng lán bǎo shí cái liào 。 ' * 5
    pin = pin.strip()
    zi_lst = []
    yin_lst = []

    for ch in han.decode('utf-8'):
        button = ui.Button(title=ch)
        button.font = ('<system>', 30)
        button.action = show_one_zi
        button.width, button.height = 80, 40
        zi_lst.append(button)

    for p in pin.decode('utf-8').split(' '):
        label = ui.Label()
        label.name = 'yin'
        label.text = p
        label.text_color = WHITE
        label.alignment = ui.ALIGN_CENTER
        label.width, label.height = 80, 40
        yin_lst.append(label)

    assert len(zi_lst) == len(yin_lst)
    num_zi = len(zi_lst)
    group_lst = []

    for i in xrange(num_zi):
        group = ui.View()
        group.width, group.height = 80, 80
        yin = yin_lst[i]
        yin.x, yin.y = group.x, group.y
        group.add_subview(yin)
        zi = zi_lst[i]
        zi.x, zi.y = group.x, group.y + zi_h
        group.add_subview(zi)
        group_lst.append(group)

    # only even number of lines
    num_col = int((view_w - hor_margin * 2) / (zi_w + zi_spacing))
    num_row = num_zi / num_col / 2 * 2
    scroll.content_size = (scroll.width, num_row * zi_h * 2 + ver_margin * 2)

    zi_count = 0
    for row in xrange(num_row):
        for col in xrange(num_col):
            try:
                if zi_count >= num_zi:
                    break
                group = group_lst[zi_count]
                group.x = scroll.x + hor_margin + (zi_w + zi_spacing) * col
                group.y = scroll.y + ver_margin + (zi_h*2 + line_spacing) * row
                scroll.add_subview(group)
                zi_count += 1

            except Exception as e:
                debug.text += str(e)
                debug.text += 'zi_count: ' + str(zi_count) + '\n'
                break

    debug.text += 'num_zi: ' + str(num_zi) + '\n'
    debug.text += 'num_row: ' + str(num_row) + '\n'

display_data()

big_button.action = show_all_zi

view.present('fullscreen')

