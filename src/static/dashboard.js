var submitReportUrl = ''
var totalSeconds = 0;
var refreshIntervalId;

function setTime() {
  ++totalSeconds;
  var minutesLabel = document.getElementById("minutes");
  var secondsLabel = document.getElementById("seconds");
  secondsLabel.innerHTML = pad(totalSeconds % 60);
  minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
  document.getElementById("timer").hidden = false;
}

function pad(val) {
    var valString = val + "";
    if (valString.length < 2) {
      return "0" + valString;
    } else {
      return valString;
    }
  }

  function stopTimer() {
    clearInterval(refreshIntervalId)
  }
  
// Populates quiz tab
function populateQuizStartPage() {
    location.hash = "";
    location.reload();
}

// Populates reports tab
function populateReports() {
    make_active('reportslink');
    $.get('reports', {},
        function (response) {
            document.getElementById("dynamicContent").innerHTML = response
        });
}

function populateAnalytics() {
    make_active('analyticslink');
    $.get('analytics', {},
        function (response) {
            console.log(response);
            document.getElementById("dynamicContent").innerHTML = response['html']

      
      //labels
      // define the chart data
      var chartData = { 
        labels : response['labels'],
        datasets : [{
            label: response['legend'],
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(75,192,192,0.4)",
            borderColor: "rgba(75,192,192,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(75,192,192,1)",
            pointBackgroundColor: "rgba(75,192,192,1)",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "#406278",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 5,
            pointHitRadius: 10,
            data : response['values'],
            spanGaps: false
        }]
      }

      // get chart canvas
      var ctx = document.getElementById("quizChart").getContext("2d");

      // create the chart using the chart canvas
      var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
        scales: {
            yAxes: [{
                ticks: {
                    max: 5,
                    min: 0,
                    stepSize: 1
                }
            }]
        }}
      });
            
        });
}

// Generates a new quiz
function generateQuiz(quiz_in_progress) {
    $loading.show();
    if (quiz_in_progress) {
        $.get('quiz?quiz_in_progress=true', {},
            function (response) {
                $loading.hide();
                document.getElementById("dynamicContent").innerHTML = response
                totalSeconds = parseInt(document.getElementById("totalSeconds").innerHTML);
                refreshIntervalId = setInterval(setTime, 1000);
            });
    }

    else {
        $.get('quiz?quiz_in_progress=false', {},
            function (response) {
                $('#timer').show();
                refreshIntervalId = setInterval(setTime, 1000);
                document.getElementById("dynamicContent").innerHTML = response
            });
    }
}

// Populates settings tab
function populateSettings() {
    make_active('settingslink');
    $.get('settings', {},
        function (response) {
            document.getElementById("dynamicContent").innerHTML = response
            $("#settingsResponse").hide();
        });
}

// Populates about tab
function populateAboutPage() {
    make_active('aboutlink');
    $.get('about', {},
        function (response) {
            document.getElementById("dynamicContent").innerHTML = response
        });
}

// Populates help page
function populateHelpPage() {
    make_active('helplink')
    $.get('help', {},
        function (response) {
            document.getElementById("dynamicContent").innerHTML = response
        })
}

// Populates navigation tab
function populateGetStartedPage() {
    make_active('getstartedlink')
    $.get('getStarted', {},
        function (response) {
            document.getElementById("dynamicContent").innerHTML = response
        })
}

// Updates quiz in progress
function updatequiz() {
    var tfval = document.getElementById("true_false").value;
    var mcval = document.getElementById("dropdown").value;
    var fillblankval = document.getElementById("fill").value;
    var nodes = document.getElementById('multiple_choice_options').childNodes;
    var multiple_choice_answers = [];

    var minutesLabel = document.getElementById("minutes");
    var secondsLabel = document.getElementById("seconds");
    secondsLabel.innerHTML = pad(totalSeconds % 60);
    minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
    
    var timetaken = minutesLabel.innerHTML + ":" + secondsLabel.innerHTML;
    for (var i = 0; i < nodes.length; i++) {
        {
            var labelChildNodes = nodes[i].childNodes;
            for (var j = 0; j < labelChildNodes.length; j++) {
                if (labelChildNodes[j].nodeName == 'INPUT' && document.getElementById(labelChildNodes[j].id).checked) {
                    if (labelChildNodes[j + 1].nodeName == '#text') {
                        multiple_choice_answers.push(labelChildNodes[j + 1].nodeValue);
                    }
                }
                j = j + 1;
            }
        }
    }
    var nodes = document.getElementById('matching').childNodes;
    var matching_prompts_answers = [];
    var matching_prompts_answer = {};
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].nodeName != '#text') {
            var labelChildNodes = nodes[i].childNodes;
            var prompt = '';
            for (var j = 0; j < labelChildNodes.length; j++) {
                if (labelChildNodes[j].nodeName != '#text') {
                    var bothsideNodes = labelChildNodes[j].childNodes;
                    for (var k = 0; k < bothsideNodes.length; k++) {
                        if (bothsideNodes[k].nodeName != '#text') {
                            if (bothsideNodes[k].nodeName == 'LABEL') {
                                prompt = bothsideNodes[k].innerHTML;
                            }
                            if (bothsideNodes[k].nodeName == 'SELECT') {
                                matching_prompts_answer[prompt] = bothsideNodes[k].value;
                            }
                        }
                    }
                }
            }

        }
    }

    var quiz_json = {
        "true_false_answer": tfval,
        "dropdown_answer": mcval,
        "fillblank_answer": fillblankval,
        "multiple_choice_answers": multiple_choice_answers,
        "matching": matching_prompts_answer,
        "timeTaken": timetaken
      }
    $.ajax({
        type: 'POST',
        url: 'updateCurrentQuizState',
        data: JSON.stringify(quiz_json),
        contentType: "application/json",
        dataType: 'json'
    });
}

// Opens chat pop up
function openForm() {
    document.getElementById("myForm").style.display = "block";
}

// Closes chat pop up
function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

// Puts the question's response received from the server in the chat text area.
function responsemessage() {
    // send request to python and get answer, update textarea
    var quiz_json = { "question": document.getElementById("typedmessage").value }
    console.log(JSON.stringify(quiz_json))
    $.ajax({
        type: 'POST',
        url: 'getHelp',
        data: JSON.stringify(quiz_json),
        success: function (data) {
            var qastring = '';
            for (i = 0; i < data.length; i++) {
                var qIndex = i + 1;
                qastring = qastring + "<br/><b>Q" + qIndex + ": " + data[i]['question'] + 
                "</b><br/>" + "Answer: " + data[i]['answer'];
            }
            document.getElementById("chatwindow").innerHTML = document.getElementById("chatwindow").innerHTML +
                "<br/><p class=\"bg-primary text-white rounded\">" +
                "Your question: " + "<b>" + document.getElementById("typedmessage").value + "</b></p><br/>" +
                'We found below help for your question' + "<br/>" + qastring + "<br/>";
            document.getElementById("typedmessage").value = '';
            var textarea = document.getElementById('chatwindow');

            textarea.scrollTop = textarea.scrollHeight;

        },
        contentType: "application/json",
        dataType: 'json'
    });

}

// document on ready function to toggle side bar icon.
$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#sidebar').toggleClass('active');
        if ($(this).find('span').text() == ">") {
            $(this).find('span').text("<");
        }
        else {
            $(this).find('span').text(">");
        }

    });
    $('#typedmessage').on('input', function () {
        if ($("#typedmessage").val().length > 0) {
            $('#sendQuestion').prop("disabled", false);
        }
        else {
            $('#sendQuestion').prop("disabled", true);
        }
    });
});

// Updates settings.
function updateSettings() {
    $("#settingsResponse").hide();
    $('#settingsform')
        .ajaxForm({
            url: 'settings',
            success: function (response) {
                $("#settingsResponse").html("Settings updated")
                $("#settingsResponse").show();
            }
        });
}

// Submits quiz and gets results to display
function submitQuiz() {
    var minutesLabel = document.getElementById("minutes");
    var secondsLabel = document.getElementById("seconds");
    secondsLabel.innerHTML = pad(totalSeconds % 60);
    minutesLabel.innerHTML = pad(parseInt(totalSeconds / 60));
    var saveUrl = "saveAndGetQuizResults?timetaken="+ minutesLabel.innerHTML + ":" + secondsLabel.innerHTML;
    $('#quizForm')
        .ajaxForm({
            url: saveUrl,
            success: function (response) {
                stopTimer();
                
                document.getElementById("quizSubmitButton").disabled = true;
                document.getElementById("toggleEnabled").disabled = true;
                console.log(response);
                $("#quizScore").html("Score: " + response['score'] + "/5");
                $("#quizScore").show();
                var results = response['results']
                for (var i = 0; i < results.length; i++) {
                    console.log(results[i]);
                    var question_div = "#" + results[i].type + "_result";
                    console.log(question_div);
                    if (results[i].boolcorrect) {
                        $(question_div).toggleClass("alert alert-success");
                        $(question_div).html("Correct!");
                    } else {
                        $(question_div).toggleClass("alert alert-danger");
                        if (results[i].type != "matching") {
                            $(question_div).html("Correct Answer: " + results[i].correct);
                        } else {
                            var correct_answer = "";
                            for (var key in results[i].correct) {
                                correct_answer += (key + "-->" + results[i].correct[key] + "<br>");
                            }
                            $(question_div).html("Correct Answer: <br>" + correct_answer);
                        }
                    }
                    $(question_div).show();
                }
                //document.getElementById("generateReport").href = response.url;
                submitReportUrl = response.url
                $("#generateReport").show();
                $("#quizScore").show();
                $("#pdfreport").show();
                document.getElementById("pdfreport").disabled = false;
                window.scrollTo(0, document.body.scrollHeight);
            }
        });
}

//Shows PDF report popup when "Print report" button is clicked
function printPDFReport() {
    windowHeight = 600;
    windowWidth = 600;
    var left = (screen.width - windowWidth) / 2;
    var top = (screen.height - windowHeight) / 4;
    QuizResultsWindow = window.open(submitReportUrl, 'QuizResultsWindow', 'width=' + windowWidth + ',height=' + windowHeight + ',top=' + top + ', left=' + left);
    return false;
}