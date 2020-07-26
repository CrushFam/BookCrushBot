*BookCrushBot* lets you suggest book of the month \(_BOTM_\) and add your favourite books to the _Roulette_\.
Under any circumstance, if you feel something is wrong, can be improved, feel free to contact
the developers\.

I have the following commands using which we can communicate\.

  ∙ /start \- Presents a gentle greeting with latest news\.
  ∙ /contact \- Shows the information required to contact the developers\.
  ∙ /help \- Gets the help message \(literally this message\)\.
  ∙ /botm \- Use this to suggest books and edit the suggested ones for _BOTM_\.
  ∙ /roulette \- Add your preferred books to the _Roulette_ using this command\.

*Discover Books*
 I can help you in conveying your book for _BOTM_ and _Roulette_\. There are three methods by which you can share the details of the book\.

 1\. _ISBN_
  Enter the International Standard Book Number \(_ISBN_\) and I will give you the book pointed by the number\.

 2\. _Name_
  Similar to a search engine, enter the name of your book and I will return the matching books\. To avoid flooding your chat, I will share only top three picks\. So describe the name as precise as possible\.

 3\. _Raw_
  If you think life will be much easier by manual description of the book, it's the place\. Fill the template with your book's fields and it will be used\.

  The structure of template is :
   _Name_ \(Book name\)
   _Author_ \(Author, if the book has multiple authors, use the first one\)
   _Genre A_ \(Genre of the book\)
   _Genre B_ \(Additional genre for clarity\)
   _Note_ \(Note for evaluator\. Keep it short\. You can use this to inform source or other identifiers of the book\)

  For your information, see that the fields are separated only by *newline*\.

 *Note*
  The API for finding book by name is not stable\.
  So the results could be senseless at times \(like incorrect _ISBN_, mismatching author\)\.
  Hence always give importance to name and author; if they are correct, proceed\.

*Removal of Books*
 1\. Removing books suggested for _BOTM_ can be done in usual way\. Choose the name of the book and it's gone for good\.
  Remember there won't be any _Yes_ or _Confirm_ prompts, once clicked, it's the decision\.

 2\. Books can not be directly removed from _Roulette_ additions, as long lists may flood the chat\. So, to prevent showing all entries, you are required to enter the name of the book\. It need not be exact name, it can be a keyword of the title\.
  All the books matching the term will be presented to you and you can continue as you would do in _BOTM_'s removal panel\.

Please be aware that while adding books for _BOTM_ and _Roulette_, if you are not active for more than five minutes, your session will expire\. The same will happen if you try to start or restart the same or another session\.

Thanks to [Open Library](http://openlibrary.org) for their API\.

Enjoy \!
