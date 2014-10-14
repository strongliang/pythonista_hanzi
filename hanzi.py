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


def button_tapped(sender):
    # pinyin = sender.superview['label1']
    for elem in view.subviews:
        if isinstance(elem, ui.Label):
            if elem.text_color == WHITE:
                elem.text_color = BLACK
                big_button.title = 'hide'
            else:
                elem.text_color = WHITE
                big_button.title = 'show'


# converting pinyin and charaters into lists are tricky
# notice the placement of spaces in the pinyin string
def init_data():
    han = '我是一个粉刷匠，粉刷本领强。'
    pin = 'Wǒ shì yī gè fěn shuā jiàng ， fěn shuā běn lǐng qiáng 。'

    zi_lst = []
    yin_lst = []

    for ch in han.decode('utf-8'):
        button = ui.Button(title=ch)
        button.font = ('<system>', 30)
        zi_lst.append(button)
    for p in pin.decode('utf-8').split(' '):
        label = ui.Label()
        label.text = p
        label.text_color = WHITE
        label.alignment = ui.ALIGN_CENTER
        yin_lst.append(label)

    assert len(zi_lst) == len(yin_lst)
    num_zi = len(zi_lst)

    debug.text += 'num_zi: ' + str(num_zi)
    # only even number of lines
    num_row = int((view_h - hor_margin * 2) / (zi_h + line_spacing)) / 2 * 2
    num_col = int((view_w - ver_margin * 2) / (zi_w + zi_spacing))

    debug.text += 'num_row: ' + str(num_row)
    debug.text += 'num_col: ' + str(num_col)

    zi_count, yin_count = 0, 0
    for row in xrange(num_row):
        for col in xrange(num_col):
            try:
                if row % 2 == 0 and yin_count < num_zi:
                    label = yin_lst.pop(0)
                    label.x = view.x + hor_margin + (zi_w + zi_spacing) * col
                    label.y = view.y + ver_margin + (zi_h + line_spacing) * row
                    label.width = 80
                    label.height = 40
                    view.add_subview(label)
                    yin_count += 1
                elif row % 2 == 1 and zi_count < num_zi:
                    button = zi_lst.pop(0)
                    button.x = view.x + hor_margin + (zi_w + zi_spacing) * col
                    button.y = view.y + ver_margin + (zi_h + line_spacing) * row
                    button.width = 80
                    button.height = 40
                    button.action = button_tapped
                    view.add_subview(button)
                    zi_count += 1
            except Exception as e:
                debug.text += str(e)
                debug.text += 'zi_count: ' + str(zi_count) + '\n'
                break

init_data()

# debug.text += 'num_zi is: ' + str(num_zi) + '\n'



big_button.action = button_tapped

view.present('sheet')
