from screen import screen

text = "© 1982 Sinclair Research Ltd."
scale_factor = 1

screen.write_text(
    text, x="centered", y=110, colour=(0, 0, 255), scale_factor=scale_factor
)

text = 'LOAD ""'
scale_factor = 3

screen.write_text(
    text, x="centered", y="centered", colour=(255, 0, 0), scale_factor=scale_factor
)
