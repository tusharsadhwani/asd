import React, { useState } from "react";
import styles from "./App.module.css";

// App.module.css
//
// .App {
//   margin: auto;
//   width: 100%;
//   max-width: 400px;
// }

// .card {
//   border: 1px solid #ccc;
//   border-radius: 5px;
//   box-shadow: 3px 3px 4px rgba(0, 0, 0, 0.3);
//   margin: 10px;
//   padding: 10px;
// }

// .btn {
//   width: 100%;
//   border: 2px solid #ccc;
//   background: white;
//   padding: 0.5em;
//   border-radius: 5px;
//   margin-bottom: 5px;
//   outline: none;
// }

export const questions = [
  {
    questionText: "What is the capital of France?",
    answerOptions: ["New York", "London", "Paris", "Dublin"],
    answerIndex: 2,
  },
  {
    questionText: "Who is CEO of Tesla?",
    answerOptions: ["Jeff Bezos", "Elon Musk", "Bill Gates", "Tony Stark"],
    answerIndex: 1,
  },
  {
    questionText: "The iPhone was created by which company?",
    answerOptions: ["Apple", "Intel", "Amazon", "Microsoft"],
    answerIndex: 0,
  },
  {
    questionText: "How many Harry Potter books are there?",
    answerOptions: ["1", "4", "6", "7"],
    answerIndex: 3,
  },
];

const App = () => {
  return (
    <div className={styles.App}>
      {questions.map((q) => (
        <Question question={q} />
      ))}
    </div>
  );
};

export default App;

export type QuestionType = {
  questionText: string;
  answerOptions: string[];
  answerIndex: number;
};

export interface QuestionProps {
  question: QuestionType;
}

const Question: React.FC<QuestionProps> = ({ question }) => {
  const [questionAnswered, setQuestionAnswered] = useState(false);

  return (
    <div className={styles.card}>
      <p>{question.questionText}</p>
      {question.answerOptions.map((ans, index) => (
        <AnswerButton
          text={ans}
          question={question}
          index={index}
          questionAnswered={questionAnswered}
          setQuestionAnswered={setQuestionAnswered}
        />
      ))}
    </div>
  );
};

export interface AnswerButtonProps {
  text: string;
  question: QuestionType;
  index: number;
  questionAnswered: boolean;
  setQuestionAnswered: (newValue: boolean) => void;
}

const AnswerButton: React.FC<AnswerButtonProps> = ({
  question,
  text,
  index,
  questionAnswered,
  setQuestionAnswered,
}) => {
  const [clicked, setClicked] = useState(false);

  return (
    <button
      className={styles.btn}
      style={{
        borderColor: clicked
          ? question.answerIndex === index
            ? "green"
            : "red"
          : undefined,
      }}
      onClick={() => {
        if (!questionAnswered) {
          setClicked(true);
          setQuestionAnswered(true);
        }
      }}
    >
      {text}
    </button>
  );
};
