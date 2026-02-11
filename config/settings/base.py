from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS = [
	"corsheaders",
	"storages",
	"modeltranslation",
	"atadizayn_website.products",
	"atadizayn_website.core",
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	"django.contrib.sites",
    "django.contrib.postgres",
    "cookie_consent",
	"django_ckeditor_5"
]

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
			],
		},
	},
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
	"default": env.db(
		"DATABASE_URL",
	)
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
	("en", "English"),
	("tr", "Türkçe"),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = "tr"

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
	AWS_LOCATION = ""  # Empty because custom domain points to bucket root

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

MODELTRANSLATION_CUSTOM_FIELDS = ('CKEditor5Field',)

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'link', '|',
            'bulletedList', 'numberedList', 'todoList', '|',
            'outdent', 'indent', '|',  # Required for nesting lists
            'insertTable', '|',
            'undo', 'redo'
        ],
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells',
                'tableProperties', 'tableCellProperties'
            ],
        },
        'list': {
            'properties': {
                'styles': True,      # Allows different bullet styles (circle, square, etc.)
                'startIndex': True,  # Allows starting ordered lists at a specific number
                'reversed': True,    # Allows reversed ordered lists
            }
        },
        'heading': {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    }
}