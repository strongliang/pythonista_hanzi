# coding: utf-8
import ui

view = ui.load_view('hanzi')

big_button = view['button1']


debug = view['textview1']
debug.text = ''

# global settings
zi_w = 80  # hanzi width
zi_h = 40  # hanzi height
hor_margin = 40  # horizontal margin
ver_margin = 40  # vertical margin

zi_spacing = 1
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
    for elem in view.subviews:
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
def init_data():
    # han = '我是一个粉刷匠，粉刷本领强。'
    # pin = 'Wǒ shì yī gè fěn shuā jiàng ， fěn shuā běn lǐng qiáng 。'
    han = '则需要满足技术指标才能获得资金，而且签订的协议阻止公司向其他公司供应蓝宝石材料。'
    pin = 'zé xū yào mǎn zú jì shù zhǐ biāo cái néng huò dé zī jīn ， ér qiě qiān dìng de xié yì zǔ zhǐ gōng sī xiàng qí tā gōng sī gōng yìng lán bǎo shí cái liào 。'
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

    # debug.text += 'num_zi: ' + str(num_zi)
    # only even number of lines
    num_row = int((view_h - hor_margin * 2) / (zi_h + line_spacing)) / 2 * 2
    num_col = int((view_w - ver_margin * 2) / (zi_w + zi_spacing))

    zi_count = 0
    for row in xrange(num_row):
        for col in xrange(num_col):
            try:
                if zi_count >= num_zi:
                    break
                group = group_lst[zi_count]
                group.x = view.x + hor_margin + (zi_w + zi_spacing) * col
                group.y = view.y + ver_margin + (zi_h*2 + line_spacing) * row
                view.add_subview(group)
                zi_count += 1

            except Exception as e:
                debug.text += str(e)
                debug.text += 'zi_count: ' + str(zi_count) + '\n'
                break

init_data()

big_button.action = show_all_zi

view.present('fullscreen')
