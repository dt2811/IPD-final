const questions = [
    {
    question: "	Have you ever experienced a terrible occurrence that has impacted you significantly? Examples may include, but are not necessarily limited to; witnessing a tragedy happen to someone else, or living through a natural disaster?",
       
    },

    {
        question: "	Do you ever feel that you have been affected by feelings of edginess, anxiety, or nerves?"

    },

    {
        question: "	Have you experienced a week or longer of lower-than-usual interest in activities that you usually enjoy? Examples might include work, exercise, or hobbies."

        
        
    },

    {
        question: "	Do feelings of anxiety or discomfort around others bother you?",
      
    },

    {
        question: "How would you describe your appetite over the past X weeks? Have your eating habits altered in any way?",
     
    },

    {
        question: "Over the last 12 months, how frequently have you felt so worried about something that you were unable to sleep at night?"
    },

    {
        question: "	Over the last 12 months, how frequently have you felt alone or lonely?"
    },

    {
        question: "How many close friends would you say you have?"
    },

    {
        question: "Tell me about any important activities or projects that you have been involved with recently. How much enjoyment do you get from these?"
    },

    {
        question: "How frequently have you been doing things that mean something to you or your life"
    },

    {
        question: "Discuss how you have been feeling about your relationships recently"
    },

    {
        question: "Tell me about how confident you have been feeling in your capabilities recently?"
    },
]
let shuffledQuestions = [] 

function handleQuestions(index) { 
    //function to shuffle and push 10 questions to shuffledQuestions array
//app would be dealing with 10questions per session
    while (shuffledQuestions.length <= 9) {
        const random = questions[Math.floor(Math.random() * questions.length)]
        if (!shuffledQuestions.includes(random)) {
            shuffledQuestions.push(random)
        }}
        NextQuestion()
    
}
function endQuiz(){
   
    document.getElementById("display-question").innerHTML="Quiz Completed"
    document.getElementById("question-no").style.display='none';
    document.getElementById("next-button").style.visibility='hidden';
    document.getElementById("submit-button").style.visibility='visible';
    document.getElementById("submit-button").style.visibility='visible';
    document.getElementById("record-button").style.visibility='hidden';

}

let questionNumber = 1 
 let indexNumber = 0 

function NextQuestion() {
    console.log("Helloo i am working")
  
    const currentQuestion = shuffledQuestions[indexNumber]
    document.getElementById("question-number").innerHTML = questionNumber;
   
    document.getElementById("display-question").innerHTML = currentQuestion.question;
    indexNumber++
    questionNumber++


}
function PreviousQuestion() {
    console.log("Helloo i am working")
    indexNumber = (indexNumber - 1 + shuffledQuestions.length) % shuffledQuestions.length
    questionNumber = (questionNumber - 1 + shuffledQuestions.length) % shuffledQuestions.length
    const currentQuestion = shuffledQuestions[indexNumber]
    document.getElementById("question-number").innerHTML = questionNumber;
   
    document.getElementById("display-question").innerHTML = currentQuestion.question;
    

}


