import mongoose from "mongoose";

const feedbackSchema = mongoose.Schema({
    prompt: {
        type: String,
        required: true,
        default: "",
        trim: true
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
}, {timestamps: true})

export const Feedback = mongoose.model("Feedback", feedbackSchema)

