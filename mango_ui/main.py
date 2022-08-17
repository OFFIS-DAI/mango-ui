from interactive import show_result_interactive

app = show_result_interactive(debug=True, no_start=True)
application = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
