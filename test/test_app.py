from mango_ui.interactive import show_result_interactive


def test_prod():
    show_result_interactive(debug=False)


def test_debug():
    show_result_interactive(debug=True)
