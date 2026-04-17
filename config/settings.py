from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent


env = environ.Env(
    DEBUG=(bool),
    SECRET_KEY=(str),
    ALLOWED_HOSTS=(list),
    DB_NAME=(str),
    DB_USER=(str),
    DB_PASSWORD=(str),
    DB_HOST=(str),
    DB_PORT=(int, 5432),
    TIME_ZONE=(str),
    SITE_ID=(int, 1),
    MEDIA_STORAGE=(str),
    CORS_ALLOWED_ORIGINS=(list),
    CSRF_TRUSTED_ORIGINS=(list),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    AWS_S3_ENDPOINT_URL=(str, ""),
    AWS_S3_REGION_NAME=(str, ""),
    AWS_S3_CUSTOM_DOMAIN=(str, ""),
    SECURE_SSL_REDIRECT=(bool),
    SECURE_HSTS_SECONDS=(int, 31536000),
    IS_BEHIND_PROXY=(bool),
)

env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

SECRET_KEY = env.str("SECRET_KEY")
DEBUG = env.bool("DEBUG")

INSTALLED_APPS = [
    "corsheaders",
    "storages",
    "modeltranslation",
    "django_ckeditor_5",
    "atadizayn_website.products",
    "atadizayn_website.core",
    "atadizayn_website.blog",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.postgres",
]

if DEBUG:
    INSTALLED_APPS += ["django_extensions"]
    INTERNAL_IPS = ["127.0.0.1"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "atadizayn_website.products.context_processors.footer_categories",
                "atadizayn_website.core.context_processors.footer_blog_collections",
                "atadizayn_website.core.context_processors.canonical_url",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "tr"

LANGUAGES = [
    ("tr", "Türkçe"),
    ("en", "English"),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = "tr"

RESERVED_CATEGORY_SLUGS = [
    "blog",
    "admin",
    "search",
    "politikalar",
    "i18n",
    "ckeditor5",
    "kitchen_sink",
    "injection-products",
    "pos-display-stands",
]

TIME_ZONE = env("TIME_ZONE")

USE_I18N = True

LOCALE_PATHS = [BASE_DIR / "locale"]

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_STORAGE = env("MEDIA_STORAGE")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

if MEDIA_STORAGE == "s3":
    AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
    AWS_DEFAULT_ACL = None
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=31536000"}
    AWS_LOCATION = ""

    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"
    STORAGES["default"] = {"BACKEND": "storages.backends.s3boto3.S3Boto3Storage"}

elif MEDIA_STORAGE == "local":
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
    STORAGES["default"] = {"BACKEND": "django.core.files.storage.FileSystemStorage"}
else:
    raise ValueError("MEDIA_STORAGE must be 'local' or 's3'.")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SITE_ID = env.int("SITE_ID")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

MODELTRANSLATION_CUSTOM_FIELDS = ("CKEditor5Field",)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"



if not DEBUG:
    SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    if env("IS_BEHIND_PROXY"):
        SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

CKEDITOR_5_CONFIGS = {
    "default": {
        "toolbar": [
            "heading",
            "|",
            "bold",
            "italic",
            "underline",
            "link",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "|",
            "outdent",
            "indent",
            "|",
            "insertTable",
            "|",
            "undo",
            "redo",
        ],
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties"],
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "toggleImageCaption",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
            ]
        },
        "list": {
            "properties": {
                "styles": True,
                "startIndex": True,
                "reversed": True,
            }
        },
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading1", "view": "h1", "title": "Heading 1", "class": "ck-heading_heading1"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
            ]
        },
    },
    "page_design": {
        "toolbar": [
            "heading",
            "|",
            "fontFamily",
            "fontSize",
            "fontColor",
            "fontBackgroundColor",
            "|",
            "bold",
            "italic",
            "underline",
            "strikethrough",
            "subscript",
            "superscript",
            "removeFormat",
            "|",
            "alignment",
            "|",
            "bulletedList",
            "numberedList",
            "todoList",
            "outdent",
            "indent",
            "|",
            "link",
            "blockQuote",
            "insertTable",
            "imageUpload",
            "mediaEmbed",
            "horizontalLine",
            "|",
            "sourceEditing",
            "|",
            "undo",
            "redo",
        ],
        "heading": {
            "options": [
                {"model": "paragraph", "title": "Paragraph", "class": "ck-heading_paragraph"},
                {"model": "heading2", "view": "h2", "title": "Heading 2", "class": "ck-heading_heading2"},
                {"model": "heading3", "view": "h3", "title": "Heading 3", "class": "ck-heading_heading3"},
                {"model": "heading4", "view": "h4", "title": "Heading 4", "class": "ck-heading_heading4"},
                {"model": "heading5", "view": "h5", "title": "Heading 5", "class": "ck-heading_heading5"},
                {"model": "heading6", "view": "h6", "title": "Heading 6", "class": "ck-heading_heading6"},
            ]
        },
        "image": {
            "toolbar": [
                "imageTextAlternative",
                "toggleImageCaption",
                "imageStyle:inline",
                "imageStyle:block",
                "imageStyle:side",
                "linkImage",
            ]
        },
        "table": {
            "contentToolbar": ["tableColumn", "tableRow", "mergeTableCells", "tableProperties", "tableCellProperties"]
        },
        "htmlSupport": {"allow": [{"name": "/^.*$/", "styles": True, "attributes": True, "classes": True}]},
    },
}

CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"
