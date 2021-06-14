dropzone.on("sending", (file, xhr, formData) => {
    formData.append('id', lectureId)
    document.querySelector("#total-progress").style.opacity = "1";
  })

  // dropzone.on("complete", () => {
  //   dropzone.removeAllFiles(true)
  // })

  dropzone.on("totaluploadprogress", function(progress) {
    document.querySelector("#total-progress .progress-bar").style.width = progress + "%";
  });

  dropzone.on("queuecomplete", function(progress) {
    document.querySelector("#total-progress").style.opacity = "0";
  });

 
  document.querySelector("#actions .cancel").onclick = function() {
    dropzone.removeAllFiles(true);
  };
