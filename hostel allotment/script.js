document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = new FormData();
    formData.append('group_info', document.querySelector('input[name="group_info"]').files[0]);
    formData.append('hostel_info', document.querySelector('input[name="hostel_info"]').files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(new Blob([blob]));
        const a = document.createElement('a');
        a.href = url;
        a.download = 'allocation_detailsAkshat.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
    });
});