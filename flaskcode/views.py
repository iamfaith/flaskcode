# -*- coding: utf-8 -*-
import os
import mimetypes
from flask import render_template, abort, jsonify, send_file, g, request, make_response
try:
    from .utils import write_file, dir_tree, get_file_extension, get_file_count
    from . import blueprint
    from .gradebook import GradeBook
except:
    from utils import write_file, dir_tree, get_file_extension, get_file_count
    from __init__ import blueprint
    from gradebook import GradeBook
import subprocess

gb = GradeBook()


@blueprint.route('/<path:current_dir>/<int:user_id>')
def main(current_dir, user_id):
    g.flaskcode_resource_basepath = g.flaskcode_resource_basepath + "/" + current_dir
    name = gb.findStudentInfoBID(user_id)
    # + "/Qidi SUN (ikun SUN)_1446817_assignsubmission_file_/lab"

    dirname = os.path.basename(g.flaskcode_resource_basepath)
    print(current_dir, user_id)
    # count = get_file_count(g.flaskcode_resource_basepath)
    dtree = {}
    if len(name) > 0:
        if len(name) == 2:
            shell_cmd = f"cd '{g.flaskcode_resource_basepath}' && ls |grep -i {name[0]}|grep -i {name[1]}"
        else:
            shell_cmd = f"cd '{g.flaskcode_resource_basepath}' && ls |grep -i {name[0]}"
        try:
            code_dir = subprocess.check_output(
                shell_cmd, shell=True, stderr=subprocess.STDOUT).decode().replace(
                '\n', '')
            g.flaskcode_resource_basepath = g.flaskcode_resource_basepath + "/" + code_dir
            dtree = dir_tree(g.flaskcode_resource_basepath, g.flaskcode_resource_basepath + '/')

        except subprocess.CalledProcessError as e:
            code_dir = e.output

    resp = make_response(
        render_template(
            'flaskcode/index.html', dirname=dirname, dtree=dtree,
            current_dir=current_dir))
    resp.set_cookie('spath', g.flaskcode_resource_basepath)
    # resp.set_cookie('base', current_dir)
    return resp


@blueprint.route('/')
def index():
    pass


@blueprint.route('/run-code/<path:file_path>', methods=['POST'])
def run_code(file_path):
    spath = request.cookies.get('spath')
    g.flaskcode_resource_basepath = spath

    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    print(file_path)
    success, message = compile_code(file_path)
    if success:
        # only success will run code
        run_dir = os.path.dirname(os.path.dirname(file_path))
        package_name = os.path.basename(os.path.dirname(file_path))
        class_name = os.path.basename(file_path).replace('.java', '')
        ret = ''
        try:
            run_shell = f"cd '{run_dir}' && java -Dfile.encoding='GBK' {package_name}.{class_name}"
            ret = subprocess.check_output(
                run_shell,
                shell=True, stderr=subprocess.STDOUT).decode("unicode_escape")

        except subprocess.CalledProcessError as e:
            ret = e.output
            try:
                ret = ret.decode()
            except:
                pass
            success = False
        message = f'Run result:[{ret}]'
        with open(f'{os.path.dirname(file_path)}/last_run.txt', "w") as f:
            f.write(ret)
    return jsonify({'success': success, 'message': message})


@blueprint.route('/resource-data/<path:file_path>.txt', methods=['GET', 'HEAD'])
def resource_data(file_path):
    spath = request.cookies.get('spath')
    g.flaskcode_resource_basepath = spath

    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)
    if not (os.path.exists(file_path) and os.path.isfile(file_path)):
        abort(404)
    response = send_file(file_path, mimetype='text/plain')
    mimetype, encoding = mimetypes.guess_type(file_path, False)
    if mimetype:
        response.headers.set('X-File-Mimetype', mimetype)
        extension = mimetypes.guess_extension(mimetype, False) or get_file_extension(file_path)
        if extension:
            response.headers.set('X-File-Extension', extension.lower().lstrip('.'))
    if encoding:
        response.headers.set('X-File-Encoding', encoding)
    return response


@blueprint.route('/update-resource-data/<path:file_path>', methods=['POST'])
def update_resource_data(file_path):
    spath = request.cookies.get('spath')
    g.flaskcode_resource_basepath = spath

    file_path = os.path.join(g.flaskcode_resource_basepath, file_path)

    isCompile = bool(int(request.form.get('isCompile', 1)))
    # print(isCompile)
    if isCompile:
        success, message = compile_code(file_path)
    else:
        success, message = clean_code(file_path)
    ############################################################## origin ########################
    # is_new_resource = bool(int(request.form.get('is_new_resource', 0)))
    # if not is_new_resource and not (os.path.exists(file_path) and os.path.isfile(file_path)):
    #     abort(404)
    # success = True
    # message = 'File saved successfully'
    # resource_data = request.form.get('resource_data', None)
    # if resource_data:
    #     success, message = write_file(resource_data, file_path)
    # else:
    #     success = False
    #     message = 'File data not uploaded'
    ############################################################## origin ########################
    return jsonify({'success': success, 'message': message})


def compile_code(file_path):
    success = True
    compile_dir = os.path.dirname(file_path)

    shell_cmd = f"cd '{compile_dir}' && javac -encoding gbk *java"
    try:
        ret = subprocess.check_output(shell_cmd, shell=True, stderr=subprocess.STDOUT)
        ret = "success"
    except subprocess.CalledProcessError as e:
        ret = e.output
        try:
            ret = ret.decode()
        except:
            pass
        success = False
    message = f'Compile result:[{ret}]'
    return success, message


def clean_code(file_path):
    success = True
    compile_dir = os.path.dirname(file_path)

    shell_cmd = f"cd '{compile_dir}' && rm *.class"
    try:
        ret = subprocess.check_output(shell_cmd, shell=True, stderr=subprocess.STDOUT)
        ret = "success"
    except subprocess.CalledProcessError as e:
        ret = e.output
        try:
            ret = ret.decode()
        except:
            pass
        success = False
    message = f'Clean result:[{ret}]'
    return success, message
