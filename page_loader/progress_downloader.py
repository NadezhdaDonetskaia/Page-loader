from progress.bar import Bar


def progress_downloader(path, data, file_name):
    file_size = int(data.headers.get('content-length', 1))
    expected_size = file_size / 1024
    progress = Bar(file_name, max=expected_size, suffix='%(percent)d%%')
    with open(path, 'wb') as f:
        progress.start()
        for chunk in data.iter_content(chunk_size=1024):
            f.write(chunk)
            progress.next()
    progress.finish()
