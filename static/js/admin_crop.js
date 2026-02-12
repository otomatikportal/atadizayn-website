(function($) {
    'use strict';

    $(document).ready(function() {
        let cropper;
        let currentFileInput;
        let $modal;
        let currentAspectRatio = 1;
        let currentOutputWidth = 1200;
        let currentOutputHeight = 1200;

        // Create a simple modal structure for cropping
        const modalHtml = `
            <div id="cropper-modal" style="display:none; position:fixed; z-index:10001; left:0; top:0; width:100%; height:100%; background:rgba(0,0,0,0.8);">
                <div style="background:#fff; margin:2% auto; padding:20px; width:80%; max-width:800px; border-radius:5px; position:relative; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                    <h3 id="cropper-modal-title" style="margin-top:0;">Görseli Kırp (1:1)</h3>
                    <div style="max-height:500px; overflow:hidden; background:#eee;">
                        <img id="cropper-image" src="" style="max-width:100%; display:block;">
                    </div>
                    <div style="margin-top:20px; text-align:right;">
                        <button type="button" id="cropper-cancel" class="button" style="background:#ccc; color:#333; margin-right:10px; border:none; padding:10px 20px; cursor:pointer;">İptal</button>
                        <button type="button" id="cropper-save" class="button" style="background:#417690; color:#fff; border:none; padding:10px 20px; cursor:pointer;">Kırp ve Kaydet</button>
                    </div>
                </div>
            </div>
        `;
        $('body').append(modalHtml);
        $modal = $('#cropper-modal');
        const $image = $('#cropper-image');
        const $modalTitle = $('#cropper-modal-title');

        // Watch for file input changes (works for inlines too)
        $(document).on('change', 'input[type="file"]', function(e) {
            const input = e.target;
            // Only trigger for image fields
            if (input.files && input.files[0] && input.files[0].type.startsWith('image/')) {
                currentFileInput = input;
                const reader = new FileReader();
                reader.onload = function(event) {
                    const aspectAttr = (input.dataset.cropAspect || '').trim();
                    let parsedAspect = NaN;
                    if (aspectAttr.includes('/')) {
                        const parts = aspectAttr.split('/').map((part) => parseFloat(part));
                        if (parts.length === 2 && Number.isFinite(parts[0]) && Number.isFinite(parts[1]) && parts[1] > 0) {
                            parsedAspect = parts[0] / parts[1];
                        }
                    } else {
                        parsedAspect = parseFloat(aspectAttr);
                    }
                    currentAspectRatio = Number.isFinite(parsedAspect) && parsedAspect > 0 ? parsedAspect : 1;

                    const widthAttr = parseInt(input.dataset.cropWidth, 10);
                    const heightAttr = parseInt(input.dataset.cropHeight, 10);
                    currentOutputWidth = Number.isFinite(widthAttr) && widthAttr > 0 ? widthAttr : 1200;
                    currentOutputHeight = Number.isFinite(heightAttr) && heightAttr > 0 ? heightAttr : Math.round(currentOutputWidth / currentAspectRatio);

                    const titleAttr = input.dataset.cropTitle;
                    $modalTitle.text(titleAttr || `Görseli Kırp (${currentAspectRatio.toFixed(2)}:1)`);

                    $image.attr('src', event.target.result);
                    $modal.show();
                    
                    if (cropper) {
                        cropper.destroy();
                    }

                    cropper = new Cropper($image[0], {
                        aspectRatio: currentAspectRatio,
                        viewMode: 1,
                        autoCropArea: 1,
                    });
                };
                reader.readAsDataURL(input.files[0]);
            }
        });

        $('#cropper-cancel').on('click', function() {
            $modal.hide();
            if (cropper) cropper.destroy();
            // Clear the input so the user can select the same file again if they want
            currentFileInput.value = '';
        });

        $('#cropper-save').on('click', function() {
            const canvas = cropper.getCroppedCanvas({
                width: currentOutputWidth,
                height: currentOutputHeight,
                imageSmoothingEnabled: true,
                imageSmoothingQuality: 'high',
            });

            canvas.toBlob(function(blob) {
                // Create a new File object from the blob to replace the input's file
                const originalFile = currentFileInput.files[0];
                const croppedFile = new File([blob], originalFile.name, {
                    type: originalFile.type,
                    lastModified: Date.now()
                });

                // Set the input's files using DataTransfer
                const dataTransfer = new DataTransfer();
                dataTransfer.items.add(croppedFile);
                currentFileInput.files = dataTransfer.files;

                // Close modal
                $modal.hide();
                cropper.destroy();
                
                // Real-time preview update
                const $row = $(currentFileInput).closest('tr, .form-row');
                const $previewImg = $row.find('.field-image_preview img, .readonly img');
                const previewUrl = URL.createObjectURL(blob);

                if ($previewImg.length) {
                    $previewImg.attr('src', previewUrl);
                } else {
                    // If no preview exists yet (new row), show it next to the file input
                    let $newPreview = $row.find('.temp-preview');
                    if ($newPreview.length === 0) {
                        $newPreview = $('<img class="temp-preview" style="max-height: 100px; border-radius: 5px; margin-top: 10px; display: block;" />');
                        $(currentFileInput).after($newPreview);
                    }
                    $newPreview.attr('src', previewUrl);
                }

                // Visual feedback in Django Admin
                const $fileInfo = $(currentFileInput).parent().find('.file-upload');
                if ($fileInfo.length) {
                    // If there's an existing link/text, update it
                    $fileInfo.contents().filter(function() {
                        return this.nodeType === 3; // Text nodes
                    }).first().replaceWith(" Kırpılmış görsel hazır. ");
                }
            }, currentFileInput.files[0].type);
        });
    });
})(django.jQuery);
