/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package information_retrieval;

import java.util.Scanner;

/**
 *
 * @author ShwetaS
 */
public class HW1_Q1 {

    //3 operations: replace, remove, insert to convert str1 to str2
    //Using Memoization
    public static int minimum(int a,int b,int c)
    {
        return(Math.min(Math.min(a,b),c));
    }
    
    public static int edit_distance(String str1, String str2,int m, int n)
    {
        int[][] temp=new int[m+1][n+1];
        for(int i=0;i<=m;i++)
        {
            for(int j=0;j<=n;j++)
            {
                if(i==0)
                    temp[i][j]=j; //j insertions if str1 is empty
                else if(j==0)
                    temp[i][j]=i; //i deletions if str2 is empty
                else if(str1.charAt(i-1)==str2.charAt(j-1)) //equal last characters, so take info of 2nd last characters
                    temp[i][j]=temp[i-1][j-1];
                else
                //When last characters of the 2 strings are not equal, minimum of the 3 edit operations is taken:
                    temp[i][j]=1+minimum(temp[i-1][j],temp[i][j-1],temp[i-1][j-1]);
                //m,n-1 case: insert
                //m-1,n case: delete
                //m-1,n-1 case: replace
            }
        }
        return temp[m][n];
    }
    public static void main(String[] args) {
        // TODO code application logic here
        Scanner in=new Scanner(System.in);
        System.out.println("Enter String 1:");
        String str1=in.nextLine();
        System.out.println("Enter String 2:");
        String str2=in.nextLine();
        int dis=edit_distance(str1,str2,str1.length(),str2.length());
        System.out.println("Edit distance to convert "+str1+" to "+str2+" is: "+dis);
    }
    
}
