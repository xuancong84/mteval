
#"   &quot;
#'   &apos;
#<   &lt;
#>   &gt;
#&   &amp;

sed "s:&:&amp;:g; s:<:\&lt;:g"

