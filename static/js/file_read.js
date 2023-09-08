// JavaScript for handling the button click and file selection

document.addEventListener('DOMContentLoaded', function () {
    var selectFileButton = document.getElementById('select-file-button');
    var fileInput = document.getElementById('file-input');
    var paraphraseTextarea = document.getElementById('paraphrase-textarea');
    var characterCounter = document.getElementById('character-counter');
    var paraphraseButton = document.getElementById('btn')

    selectFileButton.addEventListener('click', function () {
        // Trigger the file input field
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', function () {
        var file = this.files[0];
        var reader = new FileReader();

        reader.onload = function (event) {
            var fileContent = event.target.result;

            // Detect the file type based on the file's extension or content sniffing

            // Example: For PDF files
            if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
                // Use pdf.js to parse the PDF and extract its content
                pdfjsLib.getDocument(fileContent).promise.then(function (pdf) {
                    pdf.getPage(1).then(function (page) {
                        page.getTextContent().then(function (textContent) {
                            var text = '';
                            var totalCharacters = 0;
                            textContent.items.some(function (item) {
                                var itemText = item.str;
                                var itemLength = itemText.length;
                                totalCharacters += itemLength;

                                if (totalCharacters <= 400) {
                                    text += itemText;
                                } else {
                                    // If the total characters exceed 400, break the loop
                                    return true;
                                }
                            });
                            // Display the extracted content in the textarea
                            paraphraseTextarea.value = text;

                            var currentLength = paraphraseTextarea.value.length;
                            var remainingCharacters = 400 - currentLength;
                            characterCounter.textContent = remainingCharacters + ' characters remaining';
                        });
                    });
                });
            } 
            // Example: For DOCX files
            else if (file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' || file.name.endsWith('.docx')) {
                // Use docx-parser to parse the DOCX file and extract the plain text content
                DOCXParser.load(fileContent).then(function (doc) {
                    var text = doc.content;

                    // Display the extracted content in the textarea
                    paraphraseTextarea.value = text;
                });
            }
            else {
                // Handle other file types or show an error message
                paraphraseTextarea.value = 'Unsupported file type';
            }
        };

        // Read the file as binary data (arrayBuffer)
        reader.readAsArrayBuffer(file);
    });



    paraphraseTextarea.addEventListener('input', () =>{
        var currentLength = paraphraseTextarea.value.length;
        var remainingCharacters = 400 - currentLength;
        
         // Enable or disable the paraphrase button based on the textarea content
         if (paraphraseTextarea.value.trim() === '') {
            paraphraseButton.disabled = true; // Disable the button
        } else {
            paraphraseButton.disabled = false; // Enable the button
        }
        // Show the character counter or message
        if (remainingCharacters >= 0) {
            characterCounter.textContent = remainingCharacters + ' characters remaining';
        } else {
            characterCounter.textContent = 'Exceeding limit - Only 400 characters can be paraphrased at a time';
        }
    })
});