function OptionButtons({

    setAnalysisType,

    setMessages

}) {

    function choose(type) {

        setAnalysisType(type);

        setMessages([

            {

                sender: "bot",

                text:

                    `You selected ${type} analysis.

Please upload or paste the content to analyze.`

            }

        ]);

    }

    return (

        <div className="options">

            <button onClick={() => choose("Email")}>

                📧 Email

            </button>

            <button onClick={() => choose("SMS")}>

                💬 SMS

            </button>

            <button onClick={() => choose("URL")}>

                🌐 URL

            </button>

            <button onClick={() => choose("Image")}>

                🖼 Image

            </button>

        </div>

    );

}

export default OptionButtons;