# Usability Test Write-Up

## Intro  
We are a team developing a fitness-based application that includes a **Challenges feature**, where users can join challenges (steps, distance, calories) and track their progress against others.

For this usability test, participants were asked to act as a **fitness app user who wants to join and track challenges** to stay motivated.

Participants were instructed to:
- Speak out loud while interacting with the prototype  
- Explain what they think each screen does  
- Describe why they are making each action  

---

## Tasks  

### Task 1  
You want to find a challenge that tracks distance and participate in it.

### Task 2  
You want to check your progress in a challenge you joined and see how you compare to others.

---

## Notes  

### Participant 1  
- Immediately understood the "Challenges" page layout  
- Was confused between **“View” vs “Join” buttons**  
- Clicked “View” first instead of “Join”  
- Took time to realize they needed to press **“Join Challenge”** on the next screen  
- Understood progress bar clearly    

---

### Participant 2  
- Understood categories (Steps, Distance, Calories) easily  
- Tried clicking the **category tag (Distance)** thinking it was interactive  
- Liked the confirmation message after joining  
- Found leaderboard after a short delay  
- Said ranking system was clear and motivating  

---

## Feedback  

### Participant 1  
- Task difficulty: Medium  
- Confusion:  
  - Didn’t know if they were joining or just viewing  
- Suggested improvements:  
  - Make “Join” more obvious  
  - Reduce number of steps to join  
- Quote:  
  > “I feel like I had to click too many times just to join something”

---

### Participant 2  
- Task difficulty: Easy–Medium  
- Confusion:  
  - Thought category tags were clickable  
- Suggested improvements:  
  - Make buttons clearer  
  - Show join status  
- Quote:  
  > “I wasn’t sure if I already joined or not”

---

## Results  

### Issue 1: Confusion between “View” and “Join”  
- **Problem:** Users didn’t know which button joins the challenge  
- **Hypothesis:** UI does not clearly differentiate actions  
- **Fix:** Change “View” → “View Details” and highlight “Join”  

---

### Issue 2: Too many steps to join  
- **Problem:** Multiple clicks required  
- **Hypothesis:** Extra navigation creates friction  
- **Fix:** Add **Quick Join button** on main screen  

---

### Issue 3: Category labels look clickable  
- **Problem:** Users tried interacting with them  
- **Hypothesis:** Styling looks like buttons  
- **Fix:** Make them interactive filters OR redesign as labels  

---

### Issue 4: Unclear join status  
- **Problem:** Users didn’t know if they joined  
- **Hypothesis:** Lack of feedback  
- **Fix:** Add **“Joined” badge**  

---

## Updates (Prototype Changes)  

Based on feedback, the following improvements were made:

1. Added **Quick Join button** on main challenges screen  
2. Changed **“View” → “View Details”**  
3. Added **“Joined” label** for completed joins  
4. Updated category tags (either clickable or styled as labels)  
5. Improved visibility of leaderboard button  

---