from flask import make_response

def pkg_res(res):
    res = make_response(res)
    res.headers['Access-Control-Allow-Origin'] = '*'
    return res