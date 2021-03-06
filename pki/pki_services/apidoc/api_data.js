define({ "api": [
  {
    "type": "20010",
    "url": "/pki/generate_cert",
    "title": "申请生成新客户端证书",
    "name": "20010",
    "group": "ApiModule",
    "version": "0.1.0",
    "description": "<p>生成客户端证书，ext_param参数中的内容以证书扩展字段方式写入证书1.2.3.411中</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "validity_days",
            "description": "<p>有效期，单位：天</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "ext_param",
            "description": "<p>证书扩展字段内容，JSON 字符串</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "ext_param",
          "content": "{\n    \"uid\": \"\",              // 用户唯一id\n    \"gids\": [\"\", \"\"]        // 用户所有所在组id\n}",
          "type": "json"
        }
      ]
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回代码，200-成功，1-异常，2 -参数错误</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>返回消息</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data",
            "description": "<p>返回数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"code\": \"200\",\n    \"message\": \"\",\n    \"data\": {\n        \"cert_serial_no\": \"\",       // 证书序号，以此作为吊销证书接口参数\n        \"cert_create_datetime\": \"\", // '%Y-%m-%d %H:%M:%S'\n        \"cert_expire_datetime\": \"\", // '%Y-%m-%d %H:%M:%S'\n        \"private_key\": \"\",          // 证书密钥内容base64字符串\n        \"cert\": \"\",                 // 客户端证书内容base64字符串\n        \"private_key_pem_path\": \"\",  // .pem格式密钥文件下载链接\n        \"cert_pem_path\": \"\",         // .pem格式证书文件下载链接\n        \"ca_cert_pem_path\": \"\",      // .pem CA证书文件下载链接\n        \"p12_path\": \"\",              // 包含证书和密钥以及CA证书的pkcs12文件下载链接\n        \"key_file_path\": \"\",         // .key格式密钥文件\n        \"crt_file_path\": \"\",         // .crt格式证书文件下载链接\n    }\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./api/views.py",
    "groupTitle": "PKI API"
  },
  {
    "type": "20011",
    "url": "/pki/revoke_cert",
    "title": "吊销客户端证书",
    "name": "20011",
    "group": "ApiModule",
    "version": "0.1.0",
    "description": "<p>根据证书序列号吊销证书</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "cert_serial_no",
            "description": "<p>证书序列号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回代码，200-成功，1-异常，2 -参数错误</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>返回消息</p>"
          }
        ]
      }
    },
    "filename": "./api/views.py",
    "groupTitle": "PKI API"
  },
  {
    "type": "20012",
    "url": "/pki/verify_cert",
    "title": "根据证书序列号验证证书吊销状态",
    "name": "20012",
    "group": "ApiModule",
    "version": "0.1.0",
    "description": "<p>根据证书序列号验证证书是否被吊销，并不验证证书是否过期</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "cert_serial_no",
            "description": "<p>证书序列号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回代码，200-成功，1-异常，2 -参数错误</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>返回消息</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data",
            "description": "<p>返回数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"is_valid\": \"\",             // 0- 证书已被吊销，1- 合法证书\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./api/views.py",
    "groupTitle": "PKI API"
  },
  {
    "type": "20013",
    "url": "/pki/verify_cert_file",
    "title": "根据上传证书文件验证证书吊销状态",
    "name": "20013",
    "group": "ApiModule",
    "version": "0.1.0",
    "description": "<p>根据上传证书文件验证证书吊销状态，并不验证证书是否过期</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "File",
            "optional": false,
            "field": "cert_file",
            "description": "<p>证书文件，pem或p12格式</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回代码，200-成功，1-异常，2 -参数错误</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>返回消息</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data",
            "description": "<p>返回数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"is_valid\": \"\",             // 0- 证书已被吊销，1- 合法证书\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./api/views.py",
    "groupTitle": "PKI API"
  },
  {
    "type": "20014",
    "url": "/pki/query_cert_url",
    "title": "根据证书序列号获取证书文件下载地址",
    "name": "20014",
    "group": "ApiModule",
    "version": "0.1.0",
    "description": "<p>根据上传证书文件验证证书吊销状态，并不验证证书是否过期</p>",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cert_serial_no",
            "description": "<p>证书序列号</p>"
          }
        ]
      }
    },
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "type": "Integer",
            "optional": false,
            "field": "code",
            "description": "<p>返回代码，200-成功，1-异常，2 -参数错误</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "message",
            "description": "<p>返回消息</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "data",
            "description": "<p>返回数据</p>"
          }
        ]
      },
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n        \"private_key_pem_url\": \"\",  // .pem格式密钥文件下载链接\n        \"cert_pem_url\": \"\",         // .pem格式证书文件下载链接\n        \"ca_cert_pem_url\": \"\",      // .pem CA证书文件下载链接\n        \"p12_url\": \"\",              // 包含证书和密钥以及CA证书的pkcs12文件下载链接\n        \"key_file_url\": \"\",         // .key格式密钥文件\n        \"crt_file_url\": \"\",         // .crt格式证书文件下载链接\n        \"ca_crt_file_url\": \"\",      // .crt 格式CA证书文件下载链接\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./api/views.py",
    "groupTitle": "PKI API"
  },
  {
    "success": {
      "fields": {
        "Success 200": [
          {
            "group": "Success 200",
            "optional": false,
            "field": "varname1",
            "description": "<p>No type.</p>"
          },
          {
            "group": "Success 200",
            "type": "String",
            "optional": false,
            "field": "varname2",
            "description": "<p>With type.</p>"
          }
        ]
      }
    },
    "type": "",
    "url": "",
    "version": "0.0.0",
    "filename": "./apidoc/main.js",
    "group": "D__wwq_workspace_develop_projects_xtreemfs_ext_beiyuncloud_src_backend_pki_service_apidoc_main_js",
    "groupTitle": "D__wwq_workspace_develop_projects_xtreemfs_ext_beiyuncloud_src_backend_pki_service_apidoc_main_js",
    "name": ""
  }
] });
