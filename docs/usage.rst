=====
Usage
=====

To use calh in a project::

    import calh

To use calh as CLI


.. code-block:: bash

    $ calh --help

    # Visualizing calendar as a heatmap
    $ calh draw-calendar --full-year \
    --input-file examples/data/raw/ics/liverpool.ics \
    --title 'Liverpool Matches 2019/2020' \
    --output-file examples/data/processed/png/liverpool.png

To use as a web-app

    voila calh.ipynb --VoilaConfiguration.file_whitelist="['.*\.(png|ics)']"

