---
layout: post
title: My Attempt at a Mathematical Handwriting Reference
date: 2026-06-07
---

<div class="post-subheader">
I've spent way too much time thinking about this
</div>

Note: This was mostly for fun. I know a lot of people can understand their own handwriting very well and have no issues with others interpreting it, and if that works for you then there is no reason to try anything new. This reference isn't very aesthetic at all and I honestly kind of dislike it for that reason (the Greek is okay, but the English is honestly ugly). Furthermore, if you know that you aren't going to be using letters that are easy to mix up, you can just write the ones you might have gotten mixed up otherwise out normally in that specific document. At the end of the day, serious work is typed up for a reason.

Do you ever find yourself getting confused with handwritten notes from professors or peers? Have you ever made a mistake in the interpretation of your own notes because of the way you wrote out a letter or symbol? If your answer to either of these is yes, then you're spending time deciphering notation in lectures, homework, exams, projects, and labs that could have been used for understanding the actual content.

Why spend valuable time deciphering whether a symbol is meant to be $p$ or $\rho$? Why get mixed up looking back at your notes trying to figure out what is $X$ and what is $x$?

Subjects like fluid mechanics, thermodynamics, electromagnetism, statistics, and pure math are among the worst in this regard because there are a lot of instances where similar-looking letters are repeated. In fluid mechanics, $V$, $v$, $\nu$, $p$, $\rho$, $U$, $u$, and $\mu$ frequently appear in the same workflows. Consider the $y$-momentum equation for the unsteady Navier-Stokes equations in conservative form, assuming constant viscosity:

$$
\frac{\partial (\rho v)}{\partial t}
+
\frac{\partial (\rho u v)}{\partial x}
+
\frac{\partial (\rho v^2)}{\partial y}
+
\frac{\partial (\rho v w)}{\partial z}
=
-\frac{\partial p}{\partial y}
+
\frac{1}{Re_r}
\left(
\frac{\partial \tau_{xy}}{\partial x}
+
\frac{\partial \tau_{yy}}{\partial y}
+
\frac{\partial \tau_{yz}}{\partial z}
\right)
$$

Now, if you haven't had the pleasure already, imagine someone with handwriting that is anything worse than exceptional writing this out.

The simplest solution to this is to stay consistent with the way you write your letters and symbols within the document you are working on. Obviously, typing up work when things get bad is far and away the best choice. That often isn't available, so as a challenge, I've tried to come up with the most possibly clear versions of both the English and Greek alphabet that are easily readable and distinguishable for everyone to the point where it is almost unnecessary. Let's go over some important ideals for this reference. The two primary goals are to distinguish between uppercase and lowercase versions of letters and to distinguish between English and Greek letters. This should not be done using differences in size. When we are handwriting in Roman text, there are letters surrounding others, so it's easier to tell what is capitalized and what is not. In STEM, we often don't have that privilege. Thus, we should use serifs to do this whenever we need to. Another important guideline is that the strokes necessary to handwrite these should not be difficult.

## English Alphabet

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/english-alphabet-text.png" alt="English alphabet text">
    </div>
</div>

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/english-alphabet-handwritten.png" alt="English alphabet handwritten"
        style="width: 130%;">
    </div>
</div>

## Greek Alphabet

I've left out some uppercase Greek letters which are the same as the English letters and not used.

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/greek-alphabet-text.png" alt="Greek alphabet text">
    </div>
</div>

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/greek-alphabet-handwritten.png" alt="Greek alphabet handwritten"
        style="width: 130%;">
    </div>
</div>

## Numbers

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/numbers-text.png" alt="Numbers text">
    </div>
</div>

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/numbers-handwritten.png" alt="Numbers handwritten">
    </div>
</div>

## Symbols

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/various-symbols-text.png" alt="Various symbols text">
    </div>
</div>

<div class="image-block">
    <div class="image-wrapper">
        <img src="/blog-media/various-symbols-handwritten.png" alt="Various symbols handwritten">
    </div>
</div>

I have genuinely spent several years stressing out over this. The most confusing part remains distinguishing between $O$, $o$, and $0$. In case you didn't catch it, we have to unfortunately rely on size to distinguish between $O$ and $o$, while $0$ is very elongated. Additionally, it is actually challenging to distinguish between $s$ and $5$ sometimes, but that's probably a handwriting thing on my end.

## Some Notes on Notation and Syntax

Now that we know how to write out what is supposed to be italicized math text, we face the issue of Roman text. When we type up things like the $\sin$ function or Al for aluminum, they aren't in italicized math text. We of course cannot reliably handwrite italicized letters to distinguish from Roman text, so our best course of action is to write out everything using the italicized math text above.

There is still unfortunately room for confusion here, because when we are tired and more prone to mistakes, we might look at operators (which are in Roman text) next to italicized math text and think we are multiplying everything together. Richard Feynman encountered this issue as a child. He writes in Surely You're Joking, Mr. Feynman!:

"While I was doing all this trigonometry, I didn’t like the symbols for sine, cosine, tangent, and so on. To me, 'sin f' looked like s times i times n times f! So I invented another symbol, like a square root sign, that was a sigma with a long arm sticking out of it, and I put the f underneath. For the tangent it was a tau with the top of the tau extended, and for the cosine I made a kind of gamma, but it looked a little bit like the square root sign."

We are fortunate enough that context can usually resolve any ambiguities. But I still can't help but find myself wishing we had another alphabet to make these ambiguities less common in general. Here are some general tips:

- If you are using all of the following, use $*$ or simply place things next to each other for multiplication, $\cdot$ for dot product, and $\times$ for cross product if possible.
- Try to not add on unnecessary loops or curls. For instance, if you add on a loop to the bottom of an $s$, it might look like $\delta$.
- Try to always finish your strokes. Don't leave space between strokes. For instance, an incomplete $e$ might look like a $c$.
- Don't be afraid to use brackets rather than having too many parenthesis.
- Keep your English text left-aligned.
- Start a new line if you are transitioning to a new idea rather than continuing across the page in columns (maybe three columns is okay, but any more might be too cluttered).
- Make equations or expressions part of a coherent sentence rather than just dumping them on the page. You can introduce them using a clause with a colon and then put the equation or expression below. If you don't think it deserves a full line, embed it into a sentence like you would with a quote.
- Use the standard notation (or what your professor prefers) or self-descriptive variables whenever you can.
- If anything gets too complicated, just define it nearby.
- And once more, the number one thing is you being able to understand your work, so do what is the best for you (but give your future self or colleagues or whoever some leeway too)

I hope this helps, and I'm open to any suggestions.