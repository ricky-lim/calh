from pathlib import Path

import ipyvuetify as v
from ipywidgets import FileUpload

from calh.visualization import Heatmap


class App:
    def __init__(self, app_dir="."):
        self.app_dir = app_dir
        self.main_loading = v.ProgressLinear(indeterminate=False)
        self.main_toolbar = self.create_main_toolbar()
        self.heatmap_plot = v.Container()

    def create_file_upload(self) -> v.Btn:
        file_uploader = FileUpload(description=".ics file", multiple=False)

        def on_upload(change):
            self.main_loading.indeterminate = True
            value = change["new"]
            filename = list(value.keys())[0]
            uploaded_file = Path(self.app_dir) / filename
            try:
                with open(uploaded_file, "wb") as outfile:
                    outfile.write(value[filename]["content"])
                hm = Heatmap(input_data=uploaded_file)
                hm.draw(title=filename)
                self.heatmap_plot.children = [hm.result.canvas]
            finally:
                Path(uploaded_file).exists() and Path(uploaded_file).unlink()
                self.main_loading.indeterminate = False

        file_uploader.observe(on_upload, "value")
        btn_uploader = v.Btn(class_="mx-2", children=[file_uploader])
        return btn_uploader

    def create_show_example(self) -> v.Btn:
        btn = v.Btn(class_="mx-2", children=["Show example"])

        def on_click(*_):
            self.heatmap_plot.children = [
                v.Img(src="examples/data/processed/png/liverpool.png"),
            ]

        btn.on_event("click", on_click)
        return btn

    def create_link_button(self, target, text, icon):
        return v.Btn(
            class_="mx-2",
            href=target,
            target="_blank",
            children=[v.Icon(children=[icon]), text],
        )

    def create_main_toolbar(self) -> v.Toolbar:
        return v.Toolbar(
            flat=True,
            block=True,
            children=[
                v.Spacer(),
                self.create_file_upload(),
                self.create_show_example(),
                self.create_link_button(
                    target="examples/data/raw/ics/liverpool.ics",
                    text="Example Data",
                    icon="mdi-file",
                ),
                self.create_link_button(
                    target="https://github.com/ricky-lim/calh",
                    text="Source",
                    icon="mdi-github-face",
                ),
                v.Spacer(),
            ],
        )

    def create(self):
        return v.Card(
            flat=True,
            class_="mx-auto",
            children=[self.main_loading, self.main_toolbar, self.heatmap_plot],
        )
