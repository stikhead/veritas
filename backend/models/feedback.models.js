import mongoose from "mongoose";

const feedbackSchema = mongoose.Schema({
    prompt: {
        type: String,
        required: true,
        default: ""
    },

    isSatisfied: {
        type: Boolean,
        enum: [true, false],
        required: true
    },

    feedback: {
        type: String,
        maxlength: 50,
        minlength: 6
    }
}, {timestamp: true});

export const FeedbackSchema = mongoose.model("Feedback", feedbackSchema)

