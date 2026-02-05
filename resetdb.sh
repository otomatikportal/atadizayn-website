#!/bin/bash

# Hariç tutulacak dizinler (pipe | ile ayırarak ekleyebilirsin)
EXCLUDE_DIRS="venv|\.venv|env|ENV|virtualenv"

echo "--- Temizlik Islemi Baslatiliyor ---"

# 1. __pycache__ klasörlerini temizle
echo "Removing __pycache__ directories..."
find . -type d -name "__pycache__" | grep -vE "$EXCLUDE_DIRS" | xargs rm -rf 2>/dev/null

# 2. .pyc ve .pyo dosyalarını temizle
echo "Removing .pyc and .pyo files..."
find . -type f \( -name "*.pyc" -o -name "*.pyo" \) | grep -vE "$EXCLUDE_DIRS" | xargs rm -f 2>/dev/null

# 3. Migrations temizliği (__init__.py hariç)
echo "Cleaning migrations (keeping __init__.py)..."
# Önce migrations klasörlerini buluyoruz
find . -type d -name "migrations" | grep -vE "$EXCLUDE_DIRS" | while read -r mig_dir; do
    # Bu klasör içindeki .py dosyalarını bul (init hariç) ve sil
    find "$mig_dir" -type f -name "*.py" ! -name "__init__.py" -delete
    # Klasör içindeki cache'leri de temizle
    find "$mig_dir" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
done

echo "--- Islem Tamamlandi ---"