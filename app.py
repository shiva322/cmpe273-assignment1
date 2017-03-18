from flask import Flask
from github import Github
from flask import json
#import yaml
import sys

app = Flask(__name__)

@app.route('/v1/<file_param>')
def get_doc(file_param):
    g = Github("20297fa8f8fa690a06d86ecce8efcc9bc5356b72")#PersonalAccessToken

    repo = g.get_user(__username__).get_repo(__reponame__)
    filename = file_param.split(".")[0]
    fileformat = file_param.split(".")[1]

    content = repo.get_file_contents(filename+'.yml').decoded_content.strip(' ')
    config_dict = {}
    param_list = content.split('\n')
    for i in param_list:
        if i not in '':
            temp = i.split(':')
            config_dict[temp[0]] = temp[1].strip(' ').strip('"')

    if fileformat == 'json':
        response_json = app.response_class(response=json.dumps(config_dict, indent=4,
                                                               separators=(',', ': ')),
                                           status=200,
                                           mimetype='application/json')
        return response_json
    else:
        response_yaml = app.response_class(response=content,
                                           #yaml.dump(content,default_flow_style=False),
                                           status=200,
                                           mimetype='application/x-yaml')
        return response_yaml

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Invalid arguements'
        exit()

    params = sys.argv[1].split('/')
    __reponame__ = params.pop()
    __username__ = params.pop()
    app.run(debug=True, host='0.0.0.0')

