import os.path


def test_app_id_must_start_with_slash(app):
    assert app.json['id'].startswith('/')


def test_app_should_use_bridge_networking(app):
    """Apps should use bridge networking.

    There's nothing wrong with host networking and it'd be cool to use for some
    things, but it's easier to mess up, and right now nothing supports it.
    (But it's easy to accidentally write apps that sort-of work with it.)
    """
    assert app.json['container']['docker']['network'] == 'BRIDGE'


def test_app_paths_match_names(apps_path, app):
    """Apps should be in the right place in the repo."""
    assert (
        os.path.join(apps_path, app.json['id'][1:]) ==
        app.path
    )


def test_app_docker_image_has_no_tag(app):
    """Docker images should not have tags.

    Our deploy scripts change the tag each time, so we don't include tags
    in the service definitions.
    """
    image = app.json['container']['docker']['image']
    assert image is not None
    assert ':' not in image
