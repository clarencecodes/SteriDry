import os
import json
import re
from pathlib import Path

def classify_syringe(file_path):
    file_paths = [
        file_path
    ]

    project_id = '4672f201-1649-4456-990d-a3c5da251793'
    code = """curl --silent --request POST \
      --url https://app.slickk.ai/api/project/entryPoint \
      --header 'Accept: */*' \
      --header 'Accept-Language: en-US,en;q=0.5' \
      --header 'Connection: keep-alive' \
      --header 'Content-Type: multipart/form-data' \
      --form "projectId={1}" \
      {0}""".format(
        ' '.join(["--form data=@{0}".format(path) for path in file_paths]),
        project_id
    )

    # now we can execute this code
    results = os.popen(code).read()
    # the above returns a string, and it includes progress information, so let's remove that first
    results = re.sub(r'{"progress":\d+,"max":\d+}', "", results)
    # now we need to process it using the json library and load it into our program.
    results = json.loads(results)
    # now let's test it, it should print 'clean' or 'dirty'
    print(results[0]["text"])
    return results[0]["text"]
