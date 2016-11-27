import os.path


def test_app_id_must_start_with_slash(app):
    assert app.json['id'].startswith('/')


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
